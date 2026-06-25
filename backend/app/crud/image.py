from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate

class CRUDImage: 
    def get(self, db: Session, id: int, user_id: str):
        return db.query(Image).filter(Image.id == id, Image.user_id == user_id).first()
    
    def get_multi(self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        return db.query(Image).filter(Image.user_id == user_id).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ImageCreate, user_id: str):
        db_obj = Image(
            **obj_in.model_dump(),
            user_id=user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int, user_id: str):
        db_obj = self.get(db=db, id=id, user_id = user_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    image = CRUDImage()