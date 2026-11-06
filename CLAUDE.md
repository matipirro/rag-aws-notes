# CLAUDE.md

Mini-RAG sobre apuntes de AWS Cloud Practitioner: ingesta de markdown → ChromaDB local → búsqueda semántica → respuesta con Claude.

## Commands

```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# Indexar los apuntes en ./chroma_db
python -m src.ingest data/AWS-Cloud-Practitioner-Notes.md
```

## Architecture

- **`src/ingest.py`**: lee el markdown, lo trocea por secciones H2, genera embeddings (all-MiniLM-L6-v2) y los guarda en ChromaDB persistente (`./chroma_db`).
- **`src/retriever.py`**: `search(query, k=4)` devuelve los top-k chunks con score y la sección H2 de origen.
- Pendiente: `src/generator.py` (Claude), `src/api.py` (FastAPI `/ask`), tests.

## Reglas

- **Credenciales:** nunca modificar `.env` ni commitear credenciales. Verificar que `.env` esté en `.gitignore` antes de cualquier commit. El hook `.claude/hooks/protect_secrets.py` lo refuerza.
- **Entorno virtual:** verificar que el venv esté activo (el prompt muestra `(venv)`) antes de ejecutar `pip` o comandos Python.
- **Idioma:** comentarios en español, nombres de variables y funciones en inglés.
- **Commits:** nunca hacer `git commit` sin aprobación explícita del usuario.
