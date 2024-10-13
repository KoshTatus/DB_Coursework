import datetime
import enum
from typing import Annotated, Union, List, Optional, Literal
from fastapi import APIRouter, Depends, Request
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form, SelectSearchResponse
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from cruds.athletesCRUD import delete_athlete_by_id, create_athlete, get_athlete_by_id, get_all_athletes_list, \
    update_athlete_by_id, get_athletes_list, get_all_athletes
from schemas.athletes_schemas import AthleteDelete, AthleteCreate, AthleteModel, AthletesFields, AthletesSearchFields, \
    AthletesFieldsSearch
from database import get_db
from schemas.schemas import SortType

router = APIRouter()


@router.post("/api/athletes/delete")
def delete_athlete(athlete: Annotated[AthleteDelete, fastui_form(AthleteDelete)], db: Session = Depends(get_db)):
    delete_athlete_by_id(db, athlete.id)
    return [c.FireEvent(event=GoToEvent(url="/athletes"))]


@router.post("/api/athlete")
def add_athlete(form: Annotated[AthleteCreate, fastui_form(AthleteCreate)], db: Session = Depends(get_db)):
    print(form)
    create_athlete(db, form)
    return [c.FireEvent(event=GoToEvent(url='/athletes'))]


@router.post("/api/athletes/update/{athlete_id}")
def update_athlete(athlete_id: int, form: Annotated[AthleteCreate, fastui_form(AthleteCreate)],
                   db: Session = Depends(get_db)):
    update_athlete_by_id(db, athlete_id, form)
    return [c.FireEvent(event=GoToEvent(url=f"/athlete/{athlete_id}/"))]


@router.get("/api/athlete/{athlete_id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_athlete_page(athlete_id: int, db: Session = Depends(get_db)):
    res = get_athlete_by_id(db, athlete_id)

    class AthleteUpdate(BaseModel):
        first_name: str = Field(title="Имя", default=res.first_name)
        last_name: str = Field(title="Фамилия", default=res.last_name)
        date_of_birth: datetime.date = Field(title="Дата рождения", default=res.date_of_birth)
        gender: str = Field(title="Пол", default=res.gender.value)
        country_id: int = Field(title="ID страны", default=res.country_id)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url=f"/athlete/{athlete_id}/")),
                c.Heading(text='Редактировать атлета', level=2),
                c.ModelForm(
                    model=AthleteUpdate,
                    submit_url=f"/api/athletes/update/{athlete_id}",
                )
            ]
        )
    ]


@router.get("/api/athlete/{athlete_id}/", response_model=FastUI, response_model_exclude_none=True)
def athlete_profile(athlete_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    athlete = get_athlete_by_id(db, athlete_id)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/athletes")),
                c.Heading(text=athlete.first_name, level=2),
                c.Details(data=athlete),
                c.Button(text="Редактировать атлета", on_click=GoToEvent(url=f"/athlete/{athlete_id}/update")),
                c.Text(text="   "),
                c.Button(text="Удалить атлета", on_click=PageEvent(name="delete-user")),
                c.Form(
                    submit_url="/api/athletes/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=athlete_id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-user"),
                ),
            ]
        ),
    ]


class SortFormAthlete(BaseModel):
    sort_field: AthletesFields | None = Field(title="Поле сортировки", default="Имя")
    reverse: SortType | None = Field(title="Тип сортировки", default="По возрастанию")
    search_field: AthletesFieldsSearch | None = Field(title="Поле для поиска", default=None)
    search: str | None = Field(title="Поиск", default=None)

@router.post("/api/athletes/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_athletes(
        form: Annotated[SortFormAthlete, fastui_form(SortFormAthlete)],
        db: Session = Depends(get_db)
):
    print(form)
    data = get_athletes_list(
        db,
        **form.model_dump()
    )
    return [
        c.Page(
            components=[
                c.Heading(text="Результат фильтра/сортировки", level=3),
                c.Table(
                    data=data,
                    data_model=AthleteModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/athlete/{id}/')),
                        DisplayLookup(field='first_name'),
                        DisplayLookup(field='last_name'),
                        DisplayLookup(field="date_of_birth"),
                        DisplayLookup(field='gender'),
                        DisplayLookup(field='country_id', on_click=GoToEvent(url="/country/{country_id}/")),
                    ],
                    no_data_message="Нет данных по этим параметрам"
                )
            ]
        )
    ]


@router.get("/api/athletes", response_model=FastUI, response_model_exclude_none=True)
def athletes_table(
        form: Annotated[SortFormAthlete, fastui_form(SortFormAthlete)] | None = None,
        db: Session = Depends(get_db),
):
    print(form)
    data = get_all_athletes(db)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='Атлеты', level=2),
                c.ModelForm(
                    model=SortFormAthlete,
                    submit_url="api/athletes/sorting",
                    display_mode="inline",
                    method="POST",
                    submit_on_change=False,
                    submit_trigger=PageEvent(name='update'),
                ),
                c.Button(text="Подтвердить", on_click=PageEvent(name='update')),
                c.Heading(text=" ", level=2),
                c.Table(
                    data=data,
                    data_model=AthleteModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/athlete/{id}/')),
                        DisplayLookup(field='first_name'),
                        DisplayLookup(field='last_name'),
                        DisplayLookup(field="date_of_birth"),
                        DisplayLookup(field='gender'),
                        DisplayLookup(field='country_id', on_click=GoToEvent(url="/country/{country_id}/")),
                    ],
                ),
                c.Button(text="Добавить атлета", on_click=GoToEvent(url="/athlete/add")),
            ]
        )
    ]


@router.get("/api/athlete/add", response_model=FastUI, response_model_exclude_none=True)
def add_athlete_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить атлета', level=2),
                c.ModelForm(
                    model=AthleteCreate,
                    submit_url="/api/athlete",
                )
            ]
        )
    ]
