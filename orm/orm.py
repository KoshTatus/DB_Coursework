from typing import Annotated
from sqlalchemy.orm import mapped_column

from database import SessionLocal

int_primary_key = Annotated[int, mapped_column(primary_key=True)]
string_255 = Annotated[str, 255]




