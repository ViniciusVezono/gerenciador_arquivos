import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.infrastructure.persistence.database import Base
from app.api.deps import get_db, get_current_user, get_s3_storage
from app.infrastructure.storage.base import StorageClient

# SQLite em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db(db_engine) -> Generator:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

# Mock do S3 Storage
class MockStorageClient(StorageClient):
    def upload(self, file, key: str, content_type: str) -> bool:
        return True
    
    def delete(self, key: str) -> bool:
        return True
        
    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return f"http://mock-s3.com/{key}"

@pytest.fixture
def mock_storage():
    return MockStorageClient()

@pytest.fixture
def client(db, mock_storage) -> Generator:
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    def override_get_current_user():
        return "test_user_123"
        
    def override_get_s3_storage():
        return mock_storage

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_s3_storage] = override_get_s3_storage

    with TestClient(app) as c:
        yield c
