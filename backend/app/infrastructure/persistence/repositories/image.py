from typing import List
from sqlalchemy.orm import Session
from loguru import logger

from app.domain.image.entities import Image as DomainImage
from app.domain.image.repository import ImageRepository
from app.models.image import Image as ModelImage

class SQLAlchemyImageRepository(ImageRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: ModelImage) -> DomainImage:
        return DomainImage(
            id=model.id,
            user_id=model.user_id,
            filename=model.filename,
            file_key=model.file_key,
            mime_type=model.mime_type,
            size=model.size,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def create(self, image: DomainImage) -> DomainImage:
        db_obj = ModelImage(
            user_id=image.user_id,
            filename=image.filename,
            file_key=image.file_key,
            mime_type=image.mime_type,
            size=image.size
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return self._to_domain(db_obj)

    def get_by_id(self, id: int, user_id: str) -> DomainImage | None:
        db_obj = self.db.query(ModelImage).filter(ModelImage.id == id, ModelImage.user_id == user_id).first()
        if not db_obj:
            return None
        return self._to_domain(db_obj)

    def get_multi(self, user_id: str, skip: int = 0, limit: int = 100) -> List[DomainImage]:
        db_objs = self.db.query(ModelImage).filter(ModelImage.user_id == user_id).offset(skip).limit(limit).all()
        return [self._to_domain(obj) for obj in db_objs]

    def delete(self, id: int, user_id: str) -> bool:
        db_obj = self.db.query(ModelImage).filter(ModelImage.id == id, ModelImage.user_id == user_id).first()
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
