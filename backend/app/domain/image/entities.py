from dataclasses import dataclass
from datetime import datetime

@dataclass
class Image:
    id: int | None
    user_id: str
    filename: str
    file_key: str
    mime_type: str
    size: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def is_valid_size(self) -> bool:
        # Example business rule: Max size 10MB
        return self.size <= 10 * 1024 * 1024

    @property
    def is_valid_mime_type(self) -> bool:
        allowed = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        return self.mime_type in allowed
