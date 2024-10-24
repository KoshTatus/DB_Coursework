import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from cruds.generalCRUD import (
    get_all_objects,
    get_object_by_id,
    delete_object_by_id,
    update_object_by_id,
    create_object
)
from cruds.olympicsCRUD import get_olympics_list
from orm.olympics_orm import OlympicsOrm
from schemas.olympics_schemas import OlympicModel, OlympicCreate, OlympicDelete, SortFormOlympic
from database import get_db
from schemas.schemas import SeasonType

router = APIRouter()

@router.post("/api/olympic")
def add_olympic(form: Annotated[OlympicCreate, fastui_form(OlympicCreate)], db: Session = Depends(get_db)):
    create_object(db, form, OlympicsOrm)
    return [c.FireEvent(event=GoToEvent(url='/olympics'))]

@router.get("/api/olympic/add", response_model=FastUI, response_model_exclude_none=True)
def add_olympic_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить олимпиаду', level=2),
                c.ModelForm(
                    model=OlympicCreate,
                    submit_url="/api/olympic",
                )
            ]
        )
    ]

@router.post("/api/olympics/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_olympics(
        form: Annotated[SortFormOlympic, fastui_form(SortFormOlympic)],
        db: Session = Depends(get_db)
):
    data = get_olympics_list(
        db,
        **form.model_dump()
    )
    return [
        c.Page(
            components=[
                c.Heading(text="Результат фильтра/сортировки", level=3),
                c.Table(
                    data=data,
                    data_model=OlympicModel,
                    columns=[
                        DisplayLookup(field='id', title="ID", on_click=GoToEvent(url='/olympic/{id}/')),
                        DisplayLookup(field='year'),
                        DisplayLookup(field='location'),
                        DisplayLookup(field="season"),
                    ],
                    no_data_message="Нет данных по этим параметрам"
                )
            ]
        )
    ]


@router.get("/api/olympics", response_model=FastUI, response_model_exclude_none=True)
def olympics_table(
        db: Session = Depends(get_db),
):
    data = get_all_objects(db, OlympicModel, OlympicsOrm)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='Олимпиады', level=2),
                c.ModelForm(
                    model=SortFormOlympic,
                    submit_url="api/olympics/sorting",
                    display_mode="inline",
                    method="POST",
                    submit_on_change=False,
                    submit_trigger=PageEvent(name='update'),
                ),
                c.Button(text="Подтвердить", on_click=PageEvent(name='update')),
                c.Heading(text=" ", level=2),
                c.Table(
                    data=data,
                    data_model=OlympicModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/olympic/{id}/')),
                        DisplayLookup(field='location'),
                        DisplayLookup(field='year'),
                        DisplayLookup(field="season"),
                    ],
                    no_data_message="Олимпиады отсутствуют"
                ),
                c.Button(text="Добавить олимпиаду", on_click=GoToEvent(url="/olympic/add")),
            ]
        )
    ]


@router.get("/api/olympic/{id}/", response_model=FastUI, response_model_exclude_none=True)
def olympic_profile(id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    olympic = get_object_by_id(db, id, OlympicModel, OlympicsOrm)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/olympics")),
                c.Heading(text=olympic.location, level=2),
                c.Details(data=olympic),
                c.Button(text="Редактировать олимпиаду", on_click=GoToEvent(url=f"/olympic/{id}/update")),
                c.Text(text="   "),
                c.Button(text="Удалить олимпиаду", on_click=GoToEvent(url=f"/delete_olympic/{id}")),
            ]
        ),
    ]


@router.post("/api/olympics/update/{id}")
def update_olympic(id: int, form: Annotated[OlympicCreate, fastui_form(OlympicCreate)],
                   db: Session = Depends(get_db)):
    update_object_by_id(db, id, form, OlympicsOrm)
    return [c.FireEvent(event=GoToEvent(url=f"/olympic/{id}/"))]


@router.get("/api/olympic/{id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_olympic_page(id: int, db: Session = Depends(get_db)):
    res = get_object_by_id(db, id, OlympicModel, OlympicsOrm)

    class OlympicUpdate(BaseModel):
        year: datetime.time = Field(title="Год", default=res.year)
        location: str = Field(title="Место проведения", default=res.location)
        season: SeasonType = Field(title="Сезон", default=res.season)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url=f"/olympic/{id}/")),
                c.Heading(text='Редактировать олимпиаду', level=2),
                c.ModelForm(
                    model=OlympicUpdate,
                    submit_url=f"/api/olympics/update/{id}",
                )
            ]
        )
    ]


@router.post("/api/olympics/delete")
def delete_event(olympic: Annotated[OlympicDelete, fastui_form(OlympicDelete)], db: Session = Depends(get_db)):
    delete_object_by_id(db, olympic.id, OlympicsOrm)
    return [c.FireEvent(event=GoToEvent(url="/olympics"))]