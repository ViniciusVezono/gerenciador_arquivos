import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

security = HTTPBearer()

# Inicializa o JWKS client
jwks_client = jwt.PyJWKClient(settings.CLERK_JWKS_URL)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            leeway=60,
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError as e:
        logger.warning(f"Token expirado: {e}")
        raise UnauthorizedException(message="O token de autenticação expirou.", code="TOKEN_EXPIRED")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Token inválido: {type(e).__name__}: {e}")
        raise UnauthorizedException(message="Token de autenticação inválido.", code="INVALID_TOKEN")
    except Exception as e:
        logger.error(f"Erro de autenticação genérico: {type(e).__name__}: {e}")
        raise UnauthorizedException(message=f"Erro de autenticação: {str(e)}", code="AUTH_ERROR")
