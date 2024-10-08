import datetime
import enum
from typing import Annotated

from sqlalchemy import String, ForeignKey, CheckConstraint, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import Base
from schemas.schemas import GenderType, MedalType, SeasonType

int_primary_key = Annotated[int, mapped_column(primary_key=True)]
string_255 = Annotated[str, 255]


class AthletesOrm(Base):
    __tablename__ = "athletes"
    id: Mapped[int_primary_key]
    first_name: Mapped[string_255]
    last_name: Mapped[string_255]
    date_of_birth: Mapped[datetime.date] = mapped_column(CheckConstraint("date_of_birth < current_date"))
    gender: Mapped[GenderType] = mapped_column(default=GenderType.M)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="CASCADE"))


class CountriesOrm(Base):
    __tablename__ = "countries"
    id: Mapped[int_primary_key]
    country_name: Mapped[string_255] = mapped_column(unique=True)
    continent: Mapped[string_255]


class MedalsOrm(Base):
    __tablename__ = "medals"
    id: Mapped[int_primary_key]
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athletes.id", ondelete="CASCADE"))
    medal_type: Mapped[MedalType]


class OlympicsOrm(Base):
    __tablename__ = "olympics"
    id: Mapped[int_primary_key]
    year: Mapped[datetime.date]
    location: Mapped[string_255]
    season: Mapped[SeasonType]


class EventsOrm(Base):
    __tablename__ = "events"
    id: Mapped[int_primary_key]
    event_name: Mapped[string_255]
    sport_id: Mapped[int] = mapped_column(ForeignKey("sports.id", ondelete="CASCADE"))
    event_date: Mapped[datetime.date]
    olympic_id: Mapped[int] = mapped_column(ForeignKey("olympics.id", ondelete="CASCADE"))


class SportsOrm(Base):
    __tablename__ = "sports"
    id: Mapped[int_primary_key]
    sport_name: Mapped[string_255] = mapped_column(unique=True)
    category: Mapped[string_255]
