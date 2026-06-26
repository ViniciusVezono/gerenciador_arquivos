from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.storage.base import StorageClient
from app.infrastructure.storage.s3 import S3StorageClient
from app.domain.image.repository import ImageRepository
from app.infrastructure.persistence.repositories.image import SQLAlchemyImageRepository
from app.domain.image.service import ImageService
from app.core.security import get_current_user

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_s3_storage() -> StorageClient:
    return S3StorageClient()

def get_image_repository(db: Session = Depends(get_db)) -> ImageRepository:
    return SQLAlchemyImageRepository(db)

def get_image_service(
    repository: ImageRepository = Depends(get_image_repository),
    storage: StorageClient = Depends(get_s3_storage)
) -> ImageService:
    return ImageService(repository=repository, storage=storage)
