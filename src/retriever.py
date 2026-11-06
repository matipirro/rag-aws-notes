import argparse
from functools import lru_cache

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from src.config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL


@lru_cache(maxsize=1)
def _get_model():
    # Cargar el modelo tarda unos segundos: una sola vez por proceso
    return SentenceTransformer(EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def _get_collection():
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH), settings=Settings(anonymized_telemetry=False)
    )
    return client.get_collection(COLLECTION_NAME)


def search(query, k=4):
    """Devuelve los top-k chunks: [{text, section, score, distance}], mejor primero.

    score = 1 - distancia coseno (1 = idéntico, 0 = sin relación).
    """
    query_embedding = _get_model().encode([query], normalize_embeddings=True)
    results = _get_collection().query(query_embeddings=query_embedding.tolist(), n_results=k)

    return [
        {
            "text": text,
            "section": metadata["section"],
            "subsection": metadata.get("subsection", ""),
            "score": round(1 - distance, 4),
            "distance": round(distance, 4),
        }
        for text, metadata, distance in zip(
            results["documents"][0], results["metadatas"][0], results["distances"][0]
        )
    ]


if __name__ == "__main__":
    # Prueba manual: python -m src.retriever "¿qué es EC2 Auto Scaling?"
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("-k", type=int, default=4)
    args = parser.parse_args()
    for hit in search(args.query, args.k):
        print(f"[{hit['score']}] {hit['section']} › {hit['subsection']}\n  {hit['text'][:150]!r}\n")
