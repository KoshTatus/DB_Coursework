from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from orm.orm import int_primary_key
from schemas.medals_schemas import MedalType


class MedalsOrm(Base):
    __tablename__ = "medals"
    id: Mapped[int_primary_key]
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"))
    medal_type: Mapped[MedalType]