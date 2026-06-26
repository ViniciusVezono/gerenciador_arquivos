from typing import Protocol, BinaryIO

class StorageClient(Protocol):
    def upload(self, file: BinaryIO, key: str, content_type: str) -> bool:
        """Faz o upload de um arquivo para o storage."""
        ...

    def delete(self, key: str) -> bool:
        """Deleta um arquivo do storage."""
        ...

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """Gera uma URL temporária para acesso ao arquivo."""
        ...
