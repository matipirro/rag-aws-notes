# rag-aws-notes

Mini-RAG que responde preguntas sobre mis apuntes de AWS Cloud Practitioner usando búsqueda semántica local y Claude.

## Qué es

TODO: 2-3 líneas sobre el problema y por qué RAG.

## Stack

- Python 3.14
- ChromaDB (persistente local, sin servidor)
- sentence-transformers (`all-MiniLM-L6-v2`)
- Anthropic SDK (`claude-sonnet-4-5`)
- FastAPI + Uvicorn

## Cómo funciona

TODO: diagrama ingest → embeddings → ChromaDB → retrieve → Claude.

## Cómo correrlo

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # y poner tu ANTHROPIC_API_KEY

python -m src.ingest data/AWS-Cloud-Practitioner-Notes.md
```

### CLI

```bash
python cli.py "¿qué es EC2?"
```

### API

```bash
uvicorn src.api:app --reload --port 8000
```

- Documentación interactiva (Swagger, permite probar `/ask` desde el navegador): http://localhost:8000/docs
- `GET /ask?query=...&k=4` → `{"answer": "...", "sources": ["MÓDULO › subsección", ...]}`
- `query` vacío o ausente → `400`; error de la API de Claude → `502`

```bash
# -G + --data-urlencode codifica tildes, espacios y signos de la pregunta
curl -G "http://localhost:8000/ask" --data-urlencode "query=¿qué es EC2?"

# Validación: devuelve 400
curl -i "http://localhost:8000/ask?query="
```

En PowerShell, `curl` es un alias de `Invoke-WebRequest`; usa `curl.exe` o:

```powershell
Invoke-RestMethod "http://localhost:8000/ask?query=$([uri]::EscapeDataString('¿qué es EC2?'))"
```

## Ingest output

Ventanas de 200 tokens con 50 de solapamiento (`all-MiniLM-L6-v2`). Resultado: **81 chunks de 8 secciones H2** (~11.860 tokens).

| Sección | Tokens | Chunks |
|---|---:|---:|
| Introducción | 81 | 1 |
| 🗂️ Índice | 90 | 1 |
| MÓDULO 1: Introducción a la nube | 1.319 | 9 |
| MÓDULO 2: Computación en la nube | 6.366 | 43 |
| MÓDULO 3: Exploración de los servicios de computación | 3.144 | 21 |
| 📝 Preguntas tipo examen vistas | 471 | 3 |
| 🎯 Trucos para memorizar | 165 | 1 |
| 📅 Progreso | 224 | 2 |

> El Índice se omite desde que `split_by_h2` ignora `SKIP_SECTIONS`; la próxima ingesta dará 80 chunks de 7 secciones.

## Ejemplo de output

```
TODO: pregunta de ejemplo + respuesta + fuentes citadas
```

## Próximos pasos

TODO
