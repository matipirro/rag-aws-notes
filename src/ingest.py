import argparse
import re
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from src.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    OVERLAP_TOKENS,
    WINDOW_TOKENS,
)

H2_PATTERN = re.compile(r"^##\s+(.+)$")
H3_PATTERN = re.compile(r"^###\s+(.+)$")
LEADING_SYMBOLS = re.compile(r"^\W+")

# Secciones que son ruido para RAG (p. ej. la tabla de contenidos).
# Se comparan sin emojis iniciales y en minúsculas: "🗂️ Índice" → "índice"
SKIP_SECTIONS = {"índice"}


def _normalize_title(title):
    return LEADING_SYMBOLS.sub("", title).strip().lower()


def split_by_h2(markdown):
    """Devuelve [(sección, texto)]. Lo previo al primer H2 cuenta como 'Introducción'.

    Omite las secciones cuyo título está en SKIP_SECTIONS.
    """
    sections = []
    current_title = "Introducción"
    current_lines = []

    for line in markdown.splitlines():
        match = H2_PATTERN.match(line)
        if match:
            if current_lines:
                sections.append((current_title, "\n".join(current_lines).strip()))
            current_title = match.group(1).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines).strip()))

    return [
        (title, text)
        for title, text in sections
        if text and _normalize_title(title) not in SKIP_SECTIONS
    ]


def split_by_h3(text):
    """Devuelve [(subsección, cuerpo)] sin la línea del título H3.

    Lo previo al primer H3 (incluida la línea H2) queda con subsección "".
    """
    blocks = []
    current_title = ""
    current_lines = []

    for line in text.splitlines():
        match = H3_PATTERN.match(line)
        if match:
            blocks.append((current_title, "\n".join(current_lines).strip()))
            current_title = match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    blocks.append((current_title, "\n".join(current_lines).strip()))

    return [(title, body) for title, body in blocks if body]


def window_text(text, tokenizer, window=WINDOW_TOKENS, overlap=OVERLAP_TOKENS):
    """Parte el texto en ventanas de `window` tokens que se solapan `overlap` tokens.

    Usa los offsets del tokenizer para recortar el texto original: decodificar
    los tokens perdería tildes y mayúsculas (el modelo es uncased).
    """
    encoding = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    offsets = encoding["offset_mapping"]
    if not offsets:
        return []

    step = window - overlap
    windows = []
    for start in range(0, len(offsets), step):
        end = min(start + window, len(offsets))
        char_start = offsets[start][0]
        char_end = offsets[end - 1][1]
        windows.append(text[char_start:char_end])
        if end == len(offsets):
            break
    return windows


def ingest(md_path):
    markdown = Path(md_path).read_text(encoding="utf-8")
    model = SentenceTransformer(EMBEDDING_MODEL)

    chunks, metadatas = [], []
    tokenizer = model.tokenizer
    for section, text in split_by_h2(markdown):
        for subsection, body in split_by_h3(text):
            # Cada ventana lleva el título H3 delante para que no pierda contexto
            # al empezar a mitad de subsección; se descuenta del presupuesto de tokens
            prefix = f"{subsection}\n" if subsection else ""
            prefix_tokens = len(tokenizer(prefix, add_special_tokens=False)["input_ids"])
            window = WINDOW_TOKENS - prefix_tokens
            overlap = min(OVERLAP_TOKENS, window // 2)
            for i, piece in enumerate(window_text(body, tokenizer, window, overlap)):
                chunks.append(prefix + piece)
                metadatas.append(
                    {
                        "section": section,
                        "subsection": subsection,
                        "chunk_index": i,
                        "source": Path(md_path).name,
                    }
                )

    embeddings = model.encode(chunks, normalize_embeddings=True, show_progress_bar=True)

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH), settings=Settings(anonymized_telemetry=False)
    )
    # Reindexar desde cero para que correr la ingesta dos veces no duplique chunks
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

    collection.add(
        ids=[f"chunk-{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
    )

    sections = len({m["section"] for m in metadatas})
    print(f"Indexados {len(chunks)} chunks de {sections} secciones H2 en {CHROMA_PATH}")
    return len(chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indexa un markdown en ChromaDB")
    parser.add_argument("md_path")
    ingest(parser.parse_args().md_path)
