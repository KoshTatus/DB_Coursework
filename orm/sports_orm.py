from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from orm.orm import int_primary_key, string_255


class SportsOrm(Base):
    __tablename__ = "sports"
    id: Mapped[int_primary_key]
    sport_name: Mapped[string_255] = mapped_column(unique=True)
    category: Mapped[string_255]
    __table_args__ = (
        Index('sport_name_index', 'sport_name'),
    )