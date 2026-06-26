import pytest
from unittest.mock import Mock
import io

from app.domain.image.service import ImageService
from app.domain.image.entities import Image
from app.core.exceptions import AppException

def test_upload_image_success(mock_storage):
    mock_repo = Mock()
    mock_repo.create.return_value = Image(
        id=1,
        user_id="user123",
        filename="test.png",
        file_key="usuarios/user123/uuid.png",
        mime_type="image/png",
        size=1024
    )
    
    service = ImageService(repository=mock_repo, storage=mock_storage)
    file_obj = io.BytesIO(b"dummy content")
    
    image = service.upload_image(
        user_id="user123",
        filename="test.png",
        mime_type="image/png",
        size=1024,
        file_obj=file_obj
    )
    
    assert image.id == 1
    assert image.user_id == "user123"
    assert image.mime_type == "image/png"
    assert mock_repo.create.called

def test_upload_image_too_large(mock_storage):
    mock_repo = Mock()
    service = ImageService(repository=mock_repo, storage=mock_storage)
    file_obj = io.BytesIO(b"dummy content")
    
    with pytest.raises(AppException) as exc:
        service.upload_image(
            user_id="user123",
            filename="test.png",
            mime_type="image/png",
            size=20 * 1024 * 1024, # 20MB
            file_obj=file_obj
        )
        
    assert exc.value.code == "FILE_TOO_LARGE"

def test_upload_image_invalid_mime(mock_storage):
    mock_repo = Mock()
    service = ImageService(repository=mock_repo, storage=mock_storage)
    file_obj = io.BytesIO(b"dummy content")
    
    with pytest.raises(AppException) as exc:
        service.upload_image(
            user_id="user123",
            filename="test.pdf",
            mime_type="application/pdf",
            size=1024,
            file_obj=file_obj
        )
        
    assert exc.value.code == "INVALID_MIME_TYPE"
