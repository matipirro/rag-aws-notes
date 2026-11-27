# CLAUDE.md

Mini-RAG sobre apuntes de AWS Cloud Practitioner: ingesta de markdown → ChromaDB local → búsqueda semántica → respuesta con Claude.

## Commands

```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt

# Indexar los apuntes en ./chroma_db
python -m src.ingest data/AWS-Cloud-Practitioner-Notes.md

# Tests (no llaman a Claude ni necesitan chroma_db)
python -m pytest -q
```

## Architecture

- **`src/ingest.py`**: trocea el markdown por H2 → H3 → ventanas de 100 tokens (solape 25, título H3 como prefijo), genera embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) y los guarda en ChromaDB persistente (`./chroma_db`).
- **`src/retriever.py`**: `search(query, k=4)` devuelve los top-k chunks con score, sección H2 y subsección H3.
- **`src/generator.py`**: `answer(query, k)` arma el prompt con el contexto y llama a Claude.
- **`src/api.py`**: FastAPI `GET /ask`. **`cli.py`**: línea de comandos.
- **`tests/`**: troceo, generator (cliente de Claude simulado) y validación de `/ask`.

## Reglas

- **Credenciales:** nunca modificar `.env` ni commitear credenciales. Verificar que `.env` esté en `.gitignore` antes de cualquier commit. El hook `.claude/hooks/protect_secrets.py` lo refuerza.
- **Entorno virtual:** verificar que el venv esté activo (el prompt muestra `(venv)`) antes de ejecutar `pip` o comandos Python.
- **Idioma:** comentarios en español, nombres de variables y funciones en inglés.
- **Commits:** nunca hacer `git commit` sin aprobación explícita del usuario.
