from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from orm.orm import string_255, int_primary_key


class CountriesOrm(Base):
    __tablename__ = "countries"
    id: Mapped[int_primary_key]
    country_name: Mapped[string_255] = mapped_column(unique=True)
    continent: Mapped[string_255]
    __table_args__ = (
        Index('country_name_index', 'country_name'),
    )