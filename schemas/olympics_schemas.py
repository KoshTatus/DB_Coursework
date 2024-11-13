import datetime
from typing import TypeAlias, Literal
from pydantic import BaseModel, Field
from schemas.schemas import SeasonType, SortType

OlympicsFields: TypeAlias = Literal[
    "Год",
    "Место проведения",
    "Сезон"
]

OlympicsFieldsSearch: TypeAlias = Literal[
    "Место проведения",
    "Сезон"
]

OlympicsFieldsDict = {
    "Год": "year",
    "Место проведения": "location",
    "Сезон": "season"
}

class SortFormOlympic(BaseModel):
    sort_field: OlympicsFields | None = Field(title="Поле сортировки", default="Место проведения")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search_field: OlympicsFieldsSearch | None = Field(title="Фильтр", default=None)
    search: str | None = Field(title="Поиск", default=None)


class OlympicCreate(BaseModel):
    year: datetime.date = Field(title="Год проведения")
    location: str = Field(title="Место проведения")
    season: SeasonType = Field(title="Сезон")


class OlympicModel(OlympicCreate):
    id: int


class OlympicDelete(BaseModel):
    id: int
