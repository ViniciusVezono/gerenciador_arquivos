import uuid
import boto3
import jwt  
from botocore.exceptions import ClientError
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.image import ImageCreate, ImageResponse
from app.crud.image import image as crud_image
from app.core.config import settings

app = FastAPI(
    title="Gerenciador de Arquivos API",
    description="API para upload e gerenciamento de imagens",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    "s3", 
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    endpoint_url=settings.AWS_ENDPOINT_URL
)

try: 
    s3_client.create_bucket(Bucket=settings.S3_BUCKET_NAME)
    print(f"bucket '{settings.S3_BUCKET_NAME}' foi criado no ministack")
except ClientError as e: 
    if e.response['Error']['Code'] not in ['BucketAlreadyExists', 'BucketAlreadyOwnedByYou']:
        print(f"erro ao criar bucket: {e}")

security = HTTPBearer()

jwks_client = jwt.PyJWKClient(settings.CLERK_JWKS_URL)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="O token de autenticação expirou.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de autenticação inválido.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Erro de autenticação: {str(e)}")

def generate_presigned_url(file_key: str) -> str:
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.S3_BUCKET_NAME, "Key": file_key},
            ExpiresIn=3600
        )
        
        return url.replace("http://ministack:4566", "http://localhost:4566")
    
    except ClientError:
        return ""

@app.post("/images/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    file_extension = file.filename.split(".")[-1]
    file_key = f"usuarios/{user_id}/{uuid.uuid4()}.{file_extension}"

    try: 
        s3_client.upload_fileobj(
            file.file,
            settings.S3_BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": file.content_type}
        )
    except ClientError:
        raise HTTPException(status_code=500, detail="Erro interno ao fazer upload no S3.")

    image_data = ImageCreate(
        filename=file.filename,
        file_key=file_key, 
        mime_type=file.content_type,
        size=file.size or 0
    )

    return crud_image.create(db=db, obj_in=image_data, user_id=user_id)


@app.get("/images/", response_model=List[ImageResponse])
def get_images(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    db_images = crud_image.get_multi(db=db, user_id=user_id, skip=skip, limit=limit)

    for img in db_images:
        img.url = generate_presigned_url(img.file_key)
    
    return db_images

@app.get("/images/{image_id}", response_model=ImageResponse)
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) : 
    db_image = crud_image.get(db=db, id=image_id, user_id=user_id)
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Arquivo não encontrado ou sem permissão de acesso."
        )
    
    db_image.url = generate_presigned_url(db_image.file_key)
    return db_image

@app.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) :
    db_image = crud_image.get(db=db, id=image_id, user_id=user_id)
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem não encontrada"
        )

    try:
        s3_client.delete_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=db_image.file_key
        )
    except ClientError:
        raise HTTPException(status_code=500, detail="Erro interno ao deletar do S3.")


    crud_image.delete(db=db, id=image_id, user_id=user_id)
    return None


@app.get("/")
def root():
    return {"status": "ok", "message": "API rodando no Docker!"}