import datetime

from sqlalchemy.orm import Mapped

from database import Base
from orm.orm import int_primary_key, string_255
from schemas.schemas import SeasonType


class OlympicsOrm(Base):
    __tablename__ = "olympics"
    id: Mapped[int_primary_key]
    year: Mapped[datetime.date]
    location: Mapped[string_255]
    season: Mapped[SeasonType]