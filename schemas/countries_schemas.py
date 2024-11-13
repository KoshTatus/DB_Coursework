from typing import Optional, TypeAlias, Literal
from pydantic import BaseModel, Field
from schemas.schemas import SortType

CountriesFields: TypeAlias = Literal[
    "Название",
    "Континент",
]

CountriesFieldsSearch: TypeAlias = Literal[
    "Название",
    "Континент",
]

CountriesFieldsDict = {
    "Название" : "country_name",
    "Континент" : "continent",
}

class SortFormCountry(BaseModel):
    sort_field: CountriesFields | None = Field(title="Поле сортировки", default="Название")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search_field: CountriesFieldsSearch | None = Field(title="Поле для поиска", default=None)
    search: str | None = Field(title="Поиск", default=None)


class CountryCreate(BaseModel):
    country_name: str = Field(title="Название")
    continent: str = Field(title="Континент")


class CountryModel(CountryCreate):
    id: int


class CountryDelete(BaseModel):
    id: int


class CountryUpdate(BaseModel):
    id: int = Field()
    country_name: Optional[str] = Field(default=None, title="Название страны")
    continent: Optional[str] = Field(default=None)

class CountryAndCount(BaseModel):
    country_name: str = Field(title="Страна")
    count: int = Field(title="Количество")