import uuid
import boto3
from botocore.exceptions import ClientError
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
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

def get_current_user():
    return "user_vinicius"

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
    return crud_image.get_multi(db=db, user_id=user_id, skip=skip, limit=limit)

@app.get("/images/{image_id}", response_model=ImageResponse)
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
) : 
    db_image = crud_image.get(db=db, id=image_id, user_id=user_id)
    if not db_image :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagem não encontrada"
        )
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
    crud_image.delete(db=db, id=image_id, user_id=user_id)
    return None

@app.get("/")
def root():
    return {"status": "ok", "message": "API rodando no Docker!"}

@app.get("/images/{image_id}")
def get_image(image_id: int):
    return {"message": f"Buscando imagem {image_id}"}