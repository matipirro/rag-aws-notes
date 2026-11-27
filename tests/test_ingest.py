import re

from src.ingest import split_by_h2, split_by_h3, window_text


class WhitespaceTokenizer:
    """Tokenizer falso: un token por palabra, con offsets como los de HF."""

    def __call__(self, text, add_special_tokens=False, return_offsets_mapping=False):
        spans = [m.span() for m in re.finditer(r"\S+", text)]
        result = {"input_ids": list(range(len(spans)))}
        if return_offsets_mapping:
            result["offset_mapping"] = spans
        return result


# --- split_by_h2 ---


def test_split_by_h2_text_before_first_h2_is_introduction():
    md = "Texto inicial\n## Módulo 1\nContenido 1\n## Módulo 2\nContenido 2"
    sections = split_by_h2(md)

    assert [title for title, _ in sections] == ["Introducción", "Módulo 1", "Módulo 2"]
    assert sections[0][1] == "Texto inicial"
    # La línea H2 se conserva dentro del texto de su sección
    assert sections[1][1] == "## Módulo 1\nContenido 1"


def test_split_by_h2_skips_index_section_with_emoji():
    md = "## 🗂️ Índice\n- enlace\n## Módulo 1\nContenido"
    titles = [title for title, _ in split_by_h2(md)]

    assert titles == ["Módulo 1"]


def test_split_by_h2_ignores_h3_and_omits_empty_intro():
    md = "## Módulo\n### Sub\ncuerpo"
    sections = split_by_h2(md)

    assert len(sections) == 1
    assert sections[0][0] == "Módulo"


# --- split_by_h3 ---


def test_split_by_h3_strips_heading_lines():
    text = "## Módulo\nintro\n### EC2\ncuerpo ec2\n### Lambda\ncuerpo lambda"
    blocks = split_by_h3(text)

    assert blocks == [
        ("", "## Módulo\nintro"),
        ("EC2", "cuerpo ec2"),
        ("Lambda", "cuerpo lambda"),
    ]


def test_split_by_h3_drops_empty_bodies():
    text = "### Vacío\n\n### Con texto\nalgo"
    assert split_by_h3(text) == [("Con texto", "algo")]


# --- window_text ---


def test_window_text_short_text_is_single_window():
    tokenizer = WhitespaceTokenizer()
    assert window_text("uno dos tres", tokenizer, window=10, overlap=2) == ["uno dos tres"]


def test_window_text_empty_text_returns_no_windows():
    assert window_text("", WhitespaceTokenizer(), window=10, overlap=2) == []


def test_window_text_overlaps_and_covers_all_tokens():
    words = [f"w{i}" for i in range(10)]
    windows = window_text(" ".join(words), WhitespaceTokenizer(), window=4, overlap=1)

    # Paso 3: [0-3], [3-6], [6-9]
    assert windows == ["w0 w1 w2 w3", "w3 w4 w5 w6", "w6 w7 w8 w9"]


def test_window_text_preserves_original_characters():
    # Se recorta el texto original por offsets: tildes y mayúsculas intactas
    text = "Cómputo  ELÁSTICO\ncon   Auto Scaling"
    windows = window_text(text, WhitespaceTokenizer(), window=2, overlap=0)

    assert windows == ["Cómputo  ELÁSTICO", "con   Auto", "Scaling"]
