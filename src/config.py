from pathlib import Path

# Rutas y parámetros compartidos entre ingest y retriever
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_PATH = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "aws_notes"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# El multilingüe trunca a 128 tokens: 100 + [CLS]/[SEP] entra con margen
WINDOW_TOKENS = 100
OVERLAP_TOKENS = 25
