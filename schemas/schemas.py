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

class SeasonType(enum.Enum):
    summer = "summer"
    winter = "winter"


















