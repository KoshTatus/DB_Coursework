from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

url_sync = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

sync_engine = create_engine(
    url=url_sync
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=sync_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass

def create_tables_orm():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


