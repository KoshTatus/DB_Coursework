import datetime
from typing import TypeAlias, Literal
from pydantic import BaseModel, Field, field_validator
from database.database import SessionLocal
from orm.sports_orm import SportsOrm
from orm.olympics_orm import OlympicsOrm
from schemas.schemas import SortType

EventsFields: TypeAlias = Literal[
    "Название",
    "Дата"
]

EventsFieldsSearch: TypeAlias = Literal[
    "Название"
]

EventsFieldsDict = {
    "Название" : "event_name",
    "Дата" : "event_date"
}

class SortFormEvent(BaseModel):
    sort_field: EventsFields | None = Field(title="Поле сортировки", default="Название")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search: str | None = Field(title="Поиск", default=None)

class EventCreate(BaseModel):
    event_name: str = Field(title="Название")
    sport_id: int = Field(title="Sport_ID")
    event_date: datetime.date = Field(title="Дата")
    olympic_id: int = Field(title="Olympic_ID")

    @field_validator("sport_id")
    @classmethod
    def check_valid_sport_id(cls, sport_id: int) -> int:
        obj = SessionLocal().query(SportsOrm).filter(SportsOrm.id == sport_id).all()
        if len(obj) < 1:
            raise ValueError("invalid sport id!")
        return sport_id

    @field_validator("olympic_id")
    @classmethod
    def check_valid_olympic_id(cls, olympic_id: int) -> int:
        obj = SessionLocal().query(OlympicsOrm).filter(OlympicsOrm.id == olympic_id).all()
        if len(obj) < 1:
            raise ValueError("invalid olympic id!")
        return olympic_id


class EventModel(EventCreate):
    id: int = Field(title="ID")


class EventDelete(BaseModel):
    id: int