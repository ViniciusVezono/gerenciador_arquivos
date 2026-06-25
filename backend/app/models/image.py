from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class Image(Base): 
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())