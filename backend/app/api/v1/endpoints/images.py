from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status

from app.schemas.image import ImageResponse
from app.api.deps import get_current_user, get_image_service
from app.domain.image.service import ImageService

router = APIRouter()

@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    image_service: ImageService = Depends(get_image_service)
):
    image = image_service.upload_image(
        user_id=user_id,
        filename=file.filename or "unknown",
        mime_type=file.content_type or "application/octet-stream",
        size=file.size or 0,
        file_obj=file.file
    )
    
    # Gerando URL para a resposta logo após criar
    img_dict = image.__dict__.copy()
    img_dict["url"] = image_service.storage.generate_presigned_url(image.file_key)
    
    return img_dict

@router.get("/", response_model=List[ImageResponse])
def get_images(
    skip: int = 0,
    limit: int = 100,
    user_id: str = Depends(get_current_user),
    image_service: ImageService = Depends(get_image_service)
):
    return image_service.get_images(user_id=user_id, skip=skip, limit=limit)

@router.get("/{image_id}", response_model=ImageResponse)
def get_image(
    image_id: int,
    user_id: str = Depends(get_current_user),
    image_service: ImageService = Depends(get_image_service)
):
    return image_service.get_image(image_id=image_id, user_id=user_id)

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(
    image_id: int,
    user_id: str = Depends(get_current_user),
    image_service: ImageService = Depends(get_image_service)
):
    image_service.delete_image(image_id=image_id, user_id=user_id)
    return None
