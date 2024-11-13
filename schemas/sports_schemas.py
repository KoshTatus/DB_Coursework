from typing import TypeAlias, Literal
from pydantic import BaseModel, Field
from schemas.schemas import SeasonType, SortType

SportsFields: TypeAlias = Literal[
    "Название"
]

SportsFieldsSearch: TypeAlias = Literal[
    "Название",
    "Категория"
]

SportsFieldsDict = {
    "Название": "sport_name",
    "Категория": "category"
}


class SortFormSport(BaseModel):
    sort_field: SportsFields | None = Field(title="Поле сортировки", default="Название")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search_field: SportsFieldsSearch | None = Field(title="Фильтр", default=None)
    search: str | None = Field(title="Поиск", default=None)


class SportCreate(BaseModel):
    sport_name: str = Field(title="Название")
    category: SeasonType = Field(title="Сезон")


class SportModel(SportCreate):
    id: int = Field(title="ID")


class SportDelete(BaseModel):
    id: int
