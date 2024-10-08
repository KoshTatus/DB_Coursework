from database import sync_engine
from models.models import metadata


def create_tables():
    metadata.drop_all(sync_engine)
    metadata.create_all(sync_engine)


create_tables()

