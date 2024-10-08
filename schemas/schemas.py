import datetime
import enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class SortType(enum.Enum):
    true = "По убыванию"
    false = "По возрастанию"


class GenderType(enum.Enum):
    M = "M"
    F = "F"


class SortTypeForm(BaseModel):
    reverse: SortType


class AthletesFields(enum.Enum):
    first_name = "Имя"
    last_name = "Фамилия"
    date_of_birth = "Дата рождения"
    gender = "Пол"


class CountriesFields(enum.Enum):
    country_name = "country_name"
    continent = "continent"


class EventsFields(enum.Enum):
    event_name = "event_name"
    event_date = "event_date"


class SportsFields(enum.Enum):
    sport_name = "sport_name"
    category = "category"


class OlympicsFields(enum.Enum):
    year = "year"
    location = "location"
    season = "season"


class SeasonType(enum.Enum):
    summer = "summer"
    winter = "winter"


class MedalType(enum.Enum):
    gold = "gold"
    silver = "silver"
    bronze = "bronze"


class SportCreate(BaseModel):
    sport_name: str
    category: SeasonType


class SportModel(SportCreate):
    id: int


class SportDelete(BaseModel):
    id: int


class AthleteCreate(BaseModel):
    first_name: str = Field(title="Имя")
    last_name: str = Field(title="Фамилия")
    date_of_birth: datetime.date = Field(title="Дата рождения")
    gender: GenderType = Field(title="Пол")
    country_id: int = Field(title="ID страны")

    @field_validator("date_of_birth")
    @classmethod
    def check_valid_age(cls, date_of_birth: datetime.date) -> datetime.date:
        today = datetime.date.today()
        if date_of_birth > today:
            raise ValueError("invalid date of birth!")
        return date_of_birth


class AthleteModel(AthleteCreate):
    id: int


class AthleteDelete(BaseModel):
    id: int


class CountryCreate(BaseModel):
    country_name: str = Field()
    continent: str = Field()


class CountryModel(CountryCreate):
    id: int


class CountryDelete(BaseModel):
    id: int


class CountryUpdate(BaseModel):
    id: int = Field()
    country_name: Optional[str] = Field(default=None, title="Название страны")
    continent: Optional[str] = Field(default=None)


class MedalCreate(BaseModel):
    event_id: int
    athlete_id: int
    medal_type: MedalType


class MedalModel(MedalCreate):
    id: int


class MedalDelete(BaseModel):
    id: int


class OlympicCreate(BaseModel):
    year: datetime.date
    location: str
    season: SeasonType


class OlympicModel(OlympicCreate):
    id: int


class OlympicDelete(BaseModel):
    id: int


class EventCreate(BaseModel):
    event_name: str
    sport_id: int
    event_date: datetime.date
    olympic_id: int


class EventModel(EventCreate):
    id: int


class EventDelete(BaseModel):
    id: int
