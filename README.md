# rag-aws-notes

Mini-RAG que responde preguntas sobre mis apuntes de AWS Cloud Practitioner usando búsqueda semántica local y Claude.

## Qué es

Mientras preparo el examen AWS Cloud Practitioner tomo apuntes en un único markdown que ya pasa de 650 líneas, y buscar en él con Ctrl+F no sirve cuando la pregunta no usa las mismas palabras que el apunte. Este proyecto indexa los apuntes con embeddings, recupera los fragmentos relevantes para cada pregunta y le pide a Claude que responda **solo** con ese contexto, citando de qué sección sale. Si mis notas no cubren algo, lo dice en lugar de inventarlo.

## Stack

- Python 3.14
- ChromaDB 1.0 (persistente local en `./chroma_db`, sin servidor)
- sentence-transformers con `paraphrase-multilingual-MiniLM-L12-v2` (multilingüe: los apuntes y las preguntas están en español)
- Anthropic SDK con `claude-sonnet-5-5` (effort `low`, `max_tokens=2000`)
- FastAPI + Uvicorn

## Arquitectura

```
 INGESTA (una vez, o cuando cambian los apuntes)
 ──────────────────────────────────────────────────────────────────────────
  data/AWS-Cloud-Practitioner-Notes.md
        │
        ▼  split_by_h2 ─► split_by_h3        (se omite la sección "Índice")
  bloques por subsección H3
        │
        ▼  window_text: ventanas de 100 tokens, solape 25, título H3 como prefijo
  146 chunks  + metadata {section, subsection, chunk_index, source}
        │
        ▼  paraphrase-multilingual-MiniLM-L12-v2 (embeddings normalizados)
  ChromaDB  ./chroma_db  colección "aws_notes" (distancia coseno)


 CONSULTA
 ──────────────────────────────────────────────────────────────────────────
  cli.py "pregunta"          GET /ask?query=...  (src/api.py)
        └──────────┬──────────────┘
                   ▼
  src/generator.py  answer(query, k=4)
        │
        ├─► src/retriever.py  search(query, k) ──► ChromaDB ──► top-k chunks
        │
        ├─► prompt: instrucciones de sistema + contexto ([Fuente: H2 › H3] por chunk) + pregunta
        │
        ▼
  Claude (claude-sonnet-5-5)
        │
        ▼
  {"answer": "...", "sources": ["MÓDULO 2: ... › Beneficios de EC2", ...]}
```

| Archivo | Rol |
|---|---|
| `src/config.py` | Rutas, nombre de la colección, modelo de embeddings y tamaño de ventana |
| `src/ingest.py` | Trocea el markdown, genera embeddings y reconstruye la colección desde cero |
| `src/retriever.py` | `search(query, k)` devuelve chunks con `section`, `subsection` y `score` (1 − distancia coseno) |
| `src/generator.py` | `answer(query, k)` arma el prompt, llama a Claude y devuelve respuesta y fuentes |
| `src/api.py` | FastAPI: `GET /ask` |
| `cli.py` | Línea de comandos |

**Decisiones de chunking:**

- **Ventanas de 100 tokens con 25 de solape:** el modelo multilingüe trunca a 128 tokens, así que 100 más los tokens especiales entran con margen.
- **Título H3 como prefijo de cada chunk:** casi todo el temario de EC2 está bajo un único H2 ("MÓDULO 2"). Con el prefijo, una ventana que empieza a mitad de subsección no pierde su contexto, y las fuentes salen a nivel de subsección (`H2 › H3`) en lugar de repetir siempre el mismo módulo. Los tokens del prefijo se descuentan del tamaño de la ventana.

## Cómo correrlo

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # y poner tu ANTHROPIC_API_KEY

python -m src.ingest data/AWS-Cloud-Practitioner-Notes.md
```

`.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-5-5
```

### Tests

```bash
python -m pytest -q
```

Cubren el troceo (`split_by_h2`, `split_by_h3`, `window_text` con un tokenizer falso), `answer()` con el retriever y el cliente de Claude simulados, y la validación de `/ask` (200, 400, 422, 502). No consumen API ni necesitan `chroma_db`.

### CLI

```bash
python cli.py "¿qué es EC2?"
python cli.py "¿cuál es la diferencia entre EC2 y Lambda?" -k 6
```

### API

```bash
uvicorn src.api:app --reload --port 8000
```

- Documentación interactiva (Swagger, permite probar `/ask` desde el navegador): http://localhost:8000/docs
- `GET /ask?query=...&k=4` → `{"answer": "...", "sources": ["MÓDULO › subsección", ...]}`
- `k` opcional, entre 1 y 10 (por defecto 4)
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

Ventanas de 100 tokens con 25 de solape y prefijo H3 (`paraphrase-multilingual-MiniLM-L12-v2`). Resultado: **146 chunks de 7 secciones H2 y 58 subsecciones** (~9.400 tokens). La sección "🗂️ Índice" se omite por ser ruido para la búsqueda (`SKIP_SECTIONS` en `src/ingest.py`).

| Sección H2 | Bloques H3 | Tokens | Chunks |
|---|---:|---:|---:|
| Introducción | 1 | 54 | 1 |
| MÓDULO 1: Introducción a la nube | 7 | 1.032 | 16 |
| MÓDULO 2: Computación en la nube | 29 | 5.116 | 78 |
| MÓDULO 3: Exploración de los servicios de computación | 18 | 2.549 | 41 |
| 📝 Preguntas tipo examen vistas | 2 | 320 | 5 |
| 🎯 Trucos para memorizar | 1 | 115 | 2 |
| 📅 Progreso | 1 | 197 | 3 |

Los scores de similitud suelen quedar en torno a 0,5: son modestos, pero los chunks que devuelve son relevantes.

## Ejemplo de output

```
> python cli.py "¿qué es EC2?"

Según tus notas, el contexto no incluye una definición explícita de EC2 [...]. Lo que sí aparece sobre él es lo siguiente:

**Cómo funciona (3 pasos)**
- **Paso 1:** elegir la configuración de la instancia:
  - La **AMI** es la plantilla del software (equivale a elegir "qué sistema instalo").
  - El **tipo de instancia** es el tamaño del hardware virtual (equivale a "qué portátil me compro").
- **Paso 2: Conectar con la instancia.** [...] **SSH** para instancias Linux, **RDP** para instancias Windows.

**Beneficios**
- Iniciar, escalar y detener instancias rápidamente.
- Pagar solo por el tiempo de uso activo.
- Aprovisionar en minutos (frente a semanas en local).
[...]

Fuentes:
  - MÓDULO 2: Computación en la nube › Cómo funciona EC2 (3 pasos)
  - MÓDULO 2: Computación en la nube › Beneficios de EC2
  - MÓDULO 2: Computación en la nube › Los 5 tipos de instancias EC2 (TEMA ESTRELLA EXAMEN)
```

## Troubleshooting

| Síntoma | Causa | Solución |
|---|---|---|
| `SSLCertVerificationError ... self-signed certificate in certificate chain` contra `huggingface.co`, con reintentos que suman ~30 s por arranque | Un antivirus o proxy (en mi caso Kaspersky) intercepta HTTPS | `src/__init__.py` activa `HF_HUB_OFFLINE=1` porque el modelo ya está en caché. Para descargar un modelo nuevo: `HF_HUB_OFFLINE=0`, y añadir `huggingface.co` a las exclusiones del antivirus |
| `python-dotenv could not parse statement starting at line N` | Una línea del `.env` no es `CLAVE=valor` (por ejemplo, un comentario sin `#`) | Corregir esa línea. El BOM de PowerShell ya se tolera (`encoding="utf-8-sig"`) |
| `RuntimeError: Falta ANTHROPIC_API_KEY` | No existe `.env` en la raíz o no tiene la key | `cp .env.example .env` y pegar la key |
| La respuesta termina en `[respuesta truncada por max_tokens]` | Sonnet 5.5 siempre piensa antes de responder, y esos tokens cuentan contra `max_tokens` | `MAX_TOKENS = 2000` y `EFFORT = "low"` en `src/generator.py`; subir `MAX_TOKENS` si hace falta |
| `400` de la API al mandar `temperature` | Los modelos actuales rechazan los parámetros de sampling | No enviar `temperature`; usar `effort` para regular cuánto piensa el modelo |
| `UnicodeEncodeError: 'charmap' codec can't encode character` | La consola de Windows (cp1252) no puede imprimir los emojis de los títulos | `cli.py` ya fuerza UTF-8. Para otros scripts: `set PYTHONIOENCODING=utf-8` |
| `Token indices sequence length is longer than the specified maximum sequence length (N > 128)` durante la ingesta | Se tokeniza cada bloque entero para calcular los offsets de las ventanas | Inofensivo: los chunks que se indexan respetan el límite |
| La respuesta dice que falta información que sí está en los apuntes | Con `k=4`, las preguntas comparativas ("EC2 vs Lambda") reparten el contexto entre los dos temas | Subir `k` (`-k 6` en el CLI o `&k=6` en la API) |
| `curl` en PowerShell devuelve un objeto raro o falla con los parámetros | `curl` es un alias de `Invoke-WebRequest` | Usar `curl.exe` o `Invoke-RestMethod` (ver arriba) |

## Próximos pasos

- Actualizar `anthropic` (ahora `0.60.0`) para pasar `output_config` como parámetro nativo en lugar de `extra_body`
- Ajustar `k` y medir la calidad del retrieval con un set de preguntas tipo examen
- Reingestar a medida que avance el curso (módulos 4-13)
