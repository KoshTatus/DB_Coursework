import enum
from typing import TypeAlias, Literal

from pydantic import BaseModel


SortType: TypeAlias = Literal[
    "По возрастанию",
    "По убыванию"
]


class GenderType(enum.Enum):
    M = "M"
    F = "F"


class SortTypeForm(BaseModel):
    reverse: SortType












class SeasonType(enum.Enum):
    summer = "summer"
    winter = "winter"


class MedalType(enum.Enum):
    gold = "gold"
    silver = "silver"
    bronze = "bronze"

















