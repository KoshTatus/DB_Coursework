import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from cruds.athletesCRUD import get_athletes_list, create_athlete_to_country
from orm.athletes_orm import AthletesOrm
from schemas.athletes_schemas import AthleteCreate, AthleteModel, SortFormAthlete, AthleteCreateToCountry
from database import get_db
from cruds.generalCRUD import (
    get_all_objects,
    get_object_by_id,
    delete_object_by_id,
    update_object_by_id,
    create_object
)
router = APIRouter()


@router.post("/api/athlete")
def add_athlete(form: Annotated[AthleteCreate, fastui_form(AthleteCreate)], db: Session = Depends(get_db)):
    create_object(db, form, AthletesOrm)
    return [c.FireEvent(event=GoToEvent(url='/athletes'))]

@router.post("/api/athlete_country/{country_id}")
def add_athlete(country_id: int, form: Annotated[AthleteCreateToCountry, fastui_form(AthleteCreateToCountry)], db: Session = Depends(get_db)):
    create_athlete_to_country(country_id, form, db)
    return [c.FireEvent(event=GoToEvent(url='/athletes'))]

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

@router.get("/api/add_to_country/{country_id}", response_model=FastUI, response_model_exclude_none=True)
def add_athlete_to_country_page(country_id: int):
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить атлета', level=2),
                c.ModelForm(
                    model=AthleteCreateToCountry,
                    submit_url=f"/api/athlete_country/{country_id}",
                )
            ]
        )
    ]


@router.post("/api/athletes/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_athletes(
        form: Annotated[SortFormAthlete, fastui_form(SortFormAthlete)],
        db: Session = Depends(get_db)
):
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
                        DisplayLookup(field='id', title="ID", on_click=GoToEvent(url='/athlete/{id}/')),
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
        db: Session = Depends(get_db),
):
    data = get_all_objects(db, AthleteModel, AthletesOrm)
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
                    no_data_message="Атлеты отсутствуют"
                ),
                c.Button(text="Добавить атлета", on_click=GoToEvent(url="/athlete/add")),
            ]
        )
    ]


@router.get("/api/athlete/{athlete_id}/", response_model=FastUI, response_model_exclude_none=True)
def athlete_profile(athlete_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    athlete = get_object_by_id(db, athlete_id, AthleteModel, AthletesOrm)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/athletes")),
                c.Heading(text=athlete.first_name, level=2),
                c.Details(data=athlete),
                c.Button(text="Редактировать атлета", on_click=GoToEvent(url=f"/athlete/{athlete_id}/update")),
                c.Text(text="   "),
                c.Button(text="Удалить атлета", on_click=GoToEvent(url=f"/delete_athlete/{athlete_id}")),
            ]
        ),
    ]


@router.post("/api/athletes/update/{athlete_id}")
def update_athlete(athlete_id: int, form: Annotated[AthleteCreate, fastui_form(AthleteCreate)],
                   db: Session = Depends(get_db)):
    update_object_by_id(db, athlete_id, form, AthletesOrm)
    return [c.FireEvent(event=GoToEvent(url=f"/athlete/{athlete_id}/"))]


@router.get("/api/athlete/{athlete_id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_athlete_page(athlete_id: int, db: Session = Depends(get_db)):
    res = get_object_by_id(db, athlete_id, AthleteModel, AthletesOrm)

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


@router.get("/api/delete_athlete/{id}")
def delete_athlete(id: int, db: Session = Depends(get_db)):
    delete_object_by_id(db, id, AthletesOrm)
    return [c.FireEvent(event=GoToEvent(url="/athletes"))]
