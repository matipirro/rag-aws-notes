from types import SimpleNamespace

import pytest

from src import generator

HITS = [
    {"text": "EC2 son servidores virtuales", "section": "MÓDULO 2", "subsection": "Qué es EC2"},
    {"text": "Pagas por segundo", "section": "MÓDULO 2", "subsection": "Qué es EC2"},
    {"text": "Ruta de aprendizaje", "section": "Introducción", "subsection": ""},
]


class FakeMessages:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


def make_response(text, stop_reason="end_turn"):
    return SimpleNamespace(
        content=[
            SimpleNamespace(type="thinking", thinking="..."),
            SimpleNamespace(type="text", text=text),
        ],
        stop_reason=stop_reason,
    )


@pytest.fixture
def fake_claude(monkeypatch):
    """Sustituye retriever y cliente de Claude; devuelve el FakeMessages para inspeccionar."""
    messages = FakeMessages(make_response("Respuesta"))
    monkeypatch.setattr(generator, "search", lambda query, k: HITS[:k])
    monkeypatch.setattr(generator, "_get_client", lambda: SimpleNamespace(messages=messages))
    monkeypatch.delenv("CLAUDE_MODEL", raising=False)
    return messages


def test_build_context_labels_each_chunk_with_source():
    context = generator.build_context(HITS[:1] + HITS[2:])

    assert context == (
        "[Fuente: MÓDULO 2 › Qué es EC2]\nEC2 son servidores virtuales"
        "\n\n---\n\n"
        "[Fuente: Introducción]\nRuta de aprendizaje"
    )


def test_answer_returns_text_and_unique_sources_in_order(fake_claude):
    result = generator.answer("¿qué es EC2?", k=3)

    assert result == {
        "answer": "Respuesta",
        "sources": ["MÓDULO 2 › Qué es EC2", "Introducción"],
    }


def test_answer_sends_context_and_question_to_claude(fake_claude):
    generator.answer("¿qué es EC2?", k=1)

    call = fake_claude.calls[0]
    assert call["model"] == generator.DEFAULT_MODEL
    assert call["max_tokens"] == generator.MAX_TOKENS
    assert call["system"] == generator.SYSTEM_PROMPT
    assert call["extra_body"] == {"output_config": {"effort": generator.EFFORT}}
    # No se mandan parámetros de sampling: los modelos actuales los rechazan
    assert "temperature" not in call

    prompt = call["messages"][0]["content"]
    assert "EC2 son servidores virtuales" in prompt
    assert prompt.endswith("Pregunta: ¿qué es EC2?")


def test_answer_uses_model_from_env(fake_claude, monkeypatch):
    monkeypatch.setenv("CLAUDE_MODEL", "claude-haiku-5-5")
    generator.answer("hola", k=1)

    assert fake_claude.calls[0]["model"] == "claude-haiku-5-5"


def test_answer_marks_truncated_responses(fake_claude):
    fake_claude.response = make_response("Respuesta a medias", stop_reason="max_tokens")
    result = generator.answer("hola", k=1)

    assert result["answer"].endswith("[respuesta truncada por max_tokens]")


def test_get_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    generator._get_client.cache_clear()
    try:
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            generator._get_client()
    finally:
        generator._get_client.cache_clear()
