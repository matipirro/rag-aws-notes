import anthropic
from fastapi import FastAPI, HTTPException, Query

from src.generator import answer

app = FastAPI(title="rag-aws-notes", description="Preguntas sobre mis apuntes de AWS Cloud Practitioner")


# Endpoint síncrono: FastAPI lo ejecuta en un threadpool, así la llamada
# bloqueante a Claude no frena el event loop
@app.get("/ask")
def ask(
    query: str = Query("", description="Pregunta sobre los apuntes"),
    k: int = Query(4, ge=1, le=10, description="Chunks de contexto"),
):
    # Valor por defecto "" para que la query ausente también dé 400 (y no 422)
    if not query.strip():
        raise HTTPException(status_code=400, detail="El parámetro 'query' no puede estar vacío")
    try:
        return answer(query.strip(), k)
    except anthropic.APIError as e:
        raise HTTPException(status_code=502, detail=f"Error de la API de Claude: {e}") from e
