from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# configurando a inicialização do banco de dados e a conexão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()