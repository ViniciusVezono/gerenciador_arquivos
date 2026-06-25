from fastapi import FastAPI

app = FastAPI(
    title="Gerenciador de Arquivos API",
    description="API para upload e gerenciamento de imagens",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "ok", "message": "API rodando no Docker!"}

@app.get("/images/{image_id}")
def get_image(image_id: int):
    return {"message": f"Buscando imagem {image_id}"}