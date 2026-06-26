from typing import BinaryIO, List
import uuid

from loguru import logger
from app.domain.image.entities import Image
from app.domain.image.repository import ImageRepository
from app.infrastructure.storage.base import StorageClient
from app.core.exceptions import AppException, NotFoundException

class ImageService:
    def __init__(self, repository: ImageRepository, storage: StorageClient):
        self.repository = repository
        self.storage = storage

    def upload_image(self, user_id: str, filename: str, mime_type: str, size: int, file_obj: BinaryIO) -> Image:
        image = Image(
            id=None,
            user_id=user_id,
            filename=filename,
            file_key="", # Será preenchido
            mime_type=mime_type,
            size=size
        )

        if not image.is_valid_size:
            raise AppException(message="Tamanho de arquivo excede o limite de 10MB.", code="FILE_TOO_LARGE")
        
        if not image.is_valid_mime_type:
            raise AppException(message="Tipo de arquivo não permitido.", code="INVALID_MIME_TYPE")

        file_extension = filename.split(".")[-1]
        file_key = f"usuarios/{user_id}/{uuid.uuid4()}.{file_extension}"
        image.file_key = file_key

        logger.info(f"Iniciando upload de imagem para {user_id}: {filename}")
        self.storage.upload(file=file_obj, key=file_key, content_type=mime_type)

        created_image = self.repository.create(image)
        logger.info(f"Imagem {created_image.id} salva no banco com sucesso.")
        return created_image

    def get_images(self, user_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        images = self.repository.get_multi(user_id=user_id, skip=skip, limit=limit)
        
        # Gerar presigned URL para cada imagem
        result = []
        for img in images:
            img_dict = img.__dict__.copy()
            img_dict["url"] = self.storage.generate_presigned_url(img.file_key, expires_in=3600)
            result.append(img_dict)
            
        return result

    def get_image(self, image_id: int, user_id: str) -> dict:
        image = self.repository.get_by_id(id=image_id, user_id=user_id)
        if not image:
            raise NotFoundException(message="Arquivo não encontrado ou sem permissão de acesso.")
        
        img_dict = image.__dict__.copy()
        img_dict["url"] = self.storage.generate_presigned_url(image.file_key, expires_in=3600)
        return img_dict

    def delete_image(self, image_id: int, user_id: str) -> None:
        image = self.repository.get_by_id(id=image_id, user_id=user_id)
        if not image:
            raise NotFoundException(message="Imagem não encontrada")

        logger.info(f"Deletando imagem {image_id} do S3")
        self.storage.delete(key=image.file_key)

        self.repository.delete(id=image_id, user_id=user_id)
        logger.info(f"Imagem {image_id} deletada do banco.")
