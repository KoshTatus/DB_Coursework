import enum
from typing import TypeAlias, Literal
from pydantic import BaseModel, Field, field_validator
from database.database import SessionLocal
from orm.events_orm import EventsOrm
from orm.athletes_orm import AthletesOrm
from schemas.schemas import SortType

MedalsFields: TypeAlias = Literal[
    "Тип медали"
]

MedalsFieldsSearch: TypeAlias = Literal[
    "Тип медали"
]

MedalsFieldsDict = {
     "Тип медали" : "medal_type"
}

class MedalType(enum.Enum):
    gold = "gold"
    silver = "silver"
    bronze = "bronze"

class SortFormMedal(BaseModel):
    sort_field: MedalsFields | None = Field(title="Поле сортировки", default="Тип медали")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search_field: MedalType | None = Field(title="Фильтр", default=None)

class MedalCreate(BaseModel):
    event_id: int = Field(title="Event_ID")
    athlete_id: int = Field(title="Athlete_ID")
    medal_type: MedalType = Field(title="Тип")

    @field_validator("event_id")
    @classmethod
    def check_valid_event_id(cls, event_id: int) -> int:
        obj = SessionLocal().query(EventsOrm).filter(EventsOrm.id == event_id).all()
        if len(obj) < 1:
            raise ValueError("invalid event id!")
        return event_id

    @field_validator("athlete_id")
    @classmethod
    def check_valid_athlete_id(cls, athlete_id: int) -> int:
        obj = SessionLocal().query(AthletesOrm).filter(AthletesOrm.id == athlete_id).all()
        if len(obj) < 1:
            raise ValueError("invalid athlete id!")
        return athlete_id

class MedalModel(MedalCreate):
    id: int = Field(title="ID")

class MedalDelete(BaseModel):
    id: int