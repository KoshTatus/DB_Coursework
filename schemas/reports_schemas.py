import datetime
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

from schemas.medals_schemas import MedalType
from schemas.schemas import SortType

first_rep_sort_fields: TypeAlias = Literal[
    "Страна",
    "Количество атлетов",
    "Место проведения",
    "Дата начала",
]

first_rep_dict = {
    "Страна": "1",
    "Количество атлетов": "2",
    "Место проведения": "3",
    "Дата начала": "4",
}

class FirstReportFields(BaseModel):
    after: datetime.date = Field(title="После", default=datetime.date(1, 1, 1))
    before: datetime.date = Field(title="До", default=datetime.date.today())
    sort_column: first_rep_sort_fields = Field(title="Поле сортировки", default="Страна")
    sort_type: SortType = Field(title="Тип сортировки", default="По возрастанию")


second_rep_sort_fields: TypeAlias = Literal[
    "Вид спорта",
    "Количество событий",
    "Место проведения",
    "Дата начала",
]

second_rep_dict = {
    "Вид спорта": "1",
    "Количество событий": "2",
    "Место проведения": "3",
    "Дата начала": "4",
}


class SecondReportFields(BaseModel):
    after: datetime.date = Field(title="После", default=datetime.date(1, 1, 1))
    before: datetime.date = Field(title="До", default=datetime.date.today())
    sort_column: second_rep_sort_fields = Field(title="Поле сортировки", default="Вид спорта")
    sort_type: SortType = Field(title="Тип сортировки", default="По возрастанию")


third_rep_sort_fields: TypeAlias = Literal[
    "Фамилия",
    "Имя",
    "Количество медалей",
]

third_rep_dict = {
    "Фамилия" : "1",
    "Имя" : "2",
    "Количество медалей" : "3",
}

third_rep_medals_dict = {
    "gold" : "золотых",
    "silver" : "серебряных",
    "bronze" : "бронзовых"
}

class ThirdReportFields(BaseModel):
    medal_type: MedalType | None = Field(title="Тип медали", default=None)
    sort_column: third_rep_sort_fields = Field(title="Поле сортировки", default="Фамилия")
    sort_type: SortType = Field(title="Тип сортировки", default="По возрастанию")