from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel): 
    filename: str
    file_key: str
    mime_type: str
    size: int


class ImageCreate(ImageBase):
    pass

class ImageResponse(ImageBase):
    id: int
    user_id: str
    url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
