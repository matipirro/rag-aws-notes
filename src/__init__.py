import os

# El modelo de embeddings ya está en la caché local: sin esto, huggingface_hub
# consulta huggingface.co en cada arranque y falla por SSL (certificado
# autofirmado en la cadena). Se define antes de importar sentence_transformers.
# Para descargar un modelo nuevo: HF_HUB_OFFLINE=0
os.environ.setdefault("HF_HUB_OFFLINE", "1")
