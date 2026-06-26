from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.exceptions import AppException, app_exception_handler, general_exception_handler
from app.api.v1.router import api_router

logger.add("app.log", rotation="10 MB", retention="10 days", level="INFO")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para upload e gerenciamento de imagens",
    version="2.0.0" # Atualizado pós refactor
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Registra as rotas (A URL das imagens original é /images/, que ficou mapeada em api_router)
# Mas no frontend as requisições podem estar para /images e não /api/v1/images
# Então incluímos o router na raiz ou configuramos de acordo com o padrão existente
app.include_router(api_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "API rodando na nova arquitetura (v2.0.0)!"}