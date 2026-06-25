from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.image import ImageCreate, ImageResponse
from app.crud.image import image as crud_image

app = FastAPI(
    title="Gerenciador de Arquivos API",
    description="API para upload e gerenciamento de imagens",
    version="1.0.0"
)

def get_current_user():
    return "user_vinicius"

@app.post("/images/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
def create_image_metada(
    image_in: ImageCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return crud_image.create(db=db, obj_in=image_in, user_id=user_id)

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