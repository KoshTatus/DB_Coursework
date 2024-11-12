import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from orm.orm import int_primary_key, string_255


class EventsOrm(Base):
    __tablename__ = "events"
    id: Mapped[int_primary_key]
    event_name: Mapped[string_255]
    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id", ondelete="CASCADE"))
    event_date: Mapped[datetime.date]
    olympic_id: Mapped[int] = mapped_column(ForeignKey("olympics.id", ondelete="CASCADE"))