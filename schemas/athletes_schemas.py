import datetime
from typing import TypeAlias, Literal
from pydantic import BaseModel, Field, field_validator

from database.database import SessionLocal
from orm.countries_orm import CountriesOrm
from schemas.schemas import GenderType, SortType

AthletesFields: TypeAlias = Literal[
    "Имя",
    "Фамилия",
    "Дата рождения",
    "Пол"
]

AthletesFieldsSearch: TypeAlias = Literal[
    "Имя",
    "Фамилия",
    "Пол"
]

AthletesFieldsDict = {
    "Имя" : "first_name",
    "Фамилия" : "last_name",
    "Дата рождения" : "date_of_birth",
    "Пол" : "gender"
}

class SortFormAthlete(BaseModel):
    sort_field: AthletesFields | None = Field(title="Поле сортировки", default="Имя")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search_field: AthletesFieldsSearch | None = Field(title="Поле для поиска", default=None)
    search: str | None = Field(title="Поиск", default=None)

class AthleteCreateToCountry(BaseModel):
    first_name: str = Field(title="Имя")
    last_name: str = Field(title="Фамилия")
    date_of_birth: datetime.date = Field(title="Дата рождения")
    gender: GenderType = Field(title="Пол")

    @field_validator("date_of_birth")
    @classmethod
    def check_valid_age(cls, date_of_birth: datetime.date) -> datetime.date:
        today = datetime.date.today()
        if date_of_birth > today:
            raise ValueError("invalid date of birth!")
        return date_of_birth

class AthleteCreate(AthleteCreateToCountry):
    country_id: int | None = Field(title="ID страны", default=None)

    @field_validator("country_id")
    @classmethod
    def check_country_id(cls, country_id: int | None) -> int | None:
        if not country_id:
            return None
        if len(SessionLocal().query(CountriesOrm).filter(CountriesOrm.id == country_id).all()) < 1:
            raise ValueError("invalid country_id!")
        return country_id

class AthleteModel(AthleteCreate):
    id: int = Field(title="ID")


class AthleteDelete(BaseModel):
    id: int