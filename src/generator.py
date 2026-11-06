import os
from functools import lru_cache

import anthropic
from dotenv import load_dotenv

from src.config import PROJECT_ROOT
from src.retriever import search

# utf-8-sig tolera el BOM que añade PowerShell al guardar en UTF-8
load_dotenv(PROJECT_ROOT / ".env", encoding="utf-8-sig")

DEFAULT_MODEL = "claude-sonnet-5-5"
# Sonnet 5.5 piensa (thinking adaptativo) y esos tokens cuentan contra
# max_tokens: con 500 la respuesta se cortaba. Effort "low" basta para Q&A.
MAX_TOKENS = 2000
EFFORT = "low"

SYSTEM_PROMPT = (
    "Eres un asistente que responde preguntas sobre AWS Cloud Practitioner usando "
    "las notas personales de Matías. Responde SOLO con el contexto dado. "
    "Si falta información, dilo claramente."
)


@lru_cache(maxsize=1)
def _get_client():
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError("Falta ANTHROPIC_API_KEY: crea el archivo .env en la raíz del proyecto.")
    return anthropic.Anthropic()


def _source_label(hit):
    return f"{hit['section']} › {hit['subsection']}" if hit["subsection"] else hit["section"]


def build_context(hits):
    """Concatena los chunks con un separador y la sección de origen de cada uno."""
    return "\n\n---\n\n".join(f"[Fuente: {_source_label(hit)}]\n{hit['text']}" for hit in hits)


def answer(query: str, k: int = 4) -> dict:
    """Responde `query` con Claude usando los top-k chunks de las notas como contexto."""
    hits = search(query, k)
    user_prompt = f"Contexto:\n{build_context(hits)}\n\nPregunta: {query}"

    response = _get_client().messages.create(
        model=os.getenv("CLAUDE_MODEL", DEFAULT_MODEL),
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
        # anthropic==0.60.0 no tiene el parámetro output_config: va por extra_body
        extra_body={"output_config": {"effort": EFFORT}},
    )

    text = "".join(block.text for block in response.content if block.type == "text")
    if response.stop_reason == "max_tokens":
        text += "\n[respuesta truncada por max_tokens]"

    # Fuentes únicas conservando el orden de relevancia
    sources = list(dict.fromkeys(_source_label(hit) for hit in hits))
    return {"answer": text, "sources": sources}
