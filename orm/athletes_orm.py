import datetime

from sqlalchemy import Index, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from orm.orm import string_255, int_primary_key
from schemas.schemas import GenderType


class AthletesOrm(Base):
    __tablename__ = "athletes"
    id: Mapped[int_primary_key]
    first_name: Mapped[string_255]
    last_name: Mapped[string_255]
    date_of_birth: Mapped[datetime.date] = mapped_column(CheckConstraint("date_of_birth < current_date"))
    gender: Mapped[GenderType] = mapped_column(default=GenderType.M)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))
    __table_args__ = (
        Index('first_last_name_index', 'first_name', 'last_name'),
    )