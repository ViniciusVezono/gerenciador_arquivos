from typing import Protocol, List
from app.domain.image.entities import Image

class ImageRepository(Protocol):
    def create(self, image: Image) -> Image:
        """Salva uma nova imagem no banco de dados."""
        ...

    def get_by_id(self, id: int, user_id: str) -> Image | None:
        """Busca uma imagem pelo id e dono."""
        ...

    def get_multi(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Image]:
        """Busca várias imagens de um usuário."""
        ...

    def delete(self, id: int, user_id: str) -> bool:
        """Deleta uma imagem."""
        ...
