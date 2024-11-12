import datetime
import enum
from typing import TypeAlias, Literal
from pydantic import BaseModel, Field

SortType: TypeAlias = Literal[
    "По возрастанию",
    "По убыванию"
]

class GenderType(enum.Enum):
    M = "M"
    F = "F"

class SeasonType(enum.Enum):
    summer = "summer"
    winter = "winter"


class FirstReportModel(BaseModel):
    country_name: str
    count: int
    location: str
    year: datetime.date

class SecondReportModel(BaseModel):
    sport_name: str
    count: int
    location: str
    year: datetime.date

class ThirdReportModel(BaseModel):
    last_name: str
    first_name: str
    count: int














