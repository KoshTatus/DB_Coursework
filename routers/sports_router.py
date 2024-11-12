from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from cruds.sportsCRUD import get_sports_list
from orm.sports_orm import SportsOrm
from schemas.schemas import SeasonType
from schemas.sports_schemas import SportCreate, SportDelete, SportModel, SortFormSport
from database.database import get_db
from cruds.generalCRUD import (
    get_all_objects,
    get_object_by_id,
    delete_object_by_id,
    update_object_by_id,
    create_object
)

router = APIRouter()

@router.post("/api/sport")
def add_sport(form: Annotated[SportCreate, fastui_form(SportCreate)], db: Session = Depends(get_db)):
    create_object(db, form, SportsOrm)
    return [c.FireEvent(event=GoToEvent(url='/sports'))]

@router.get("/api/sport/add", response_model=FastUI, response_model_exclude_none=True)
def add_sport_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить спорт', level=2),
                c.ModelForm(
                    model=SportCreate,
                    submit_url="/api/sport"
                )
            ]
        )
    ]


@router.post("/api/sports/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_sports(
        form: Annotated[SortFormSport, fastui_form(SortFormSport)],
        db: Session = Depends(get_db)
):
    data = get_sports_list(
        db,
        **form.model_dump()
    )
    return [
        c.Page(
            components=[
                c.Heading(text="Результат фильтра/сортировки", level=3),
                c.Table(
                    data=data,
                    data_model=SportModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/sport/{id}/')),
                        DisplayLookup(field='sport_name'),
                        DisplayLookup(field='category'),
                    ],
                    no_data_message="Нет данных по этим параметрам"
                ),
            ]
        )
    ]


@router.get("/api/sports", response_model=FastUI, response_model_exclude_none=True)
def sports_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    data = get_all_objects(db, SportModel, SportsOrm)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='Виды спорта', level=2),
                c.ModelForm(
                    model=SortFormSport,
                    submit_url="api/sports/sorting",
                    display_mode="inline",
                    method="POST",
                    submit_on_change=False,
                    submit_trigger=PageEvent(name='update'),
                ),
                c.Button(text="Подтвердить", on_click=PageEvent(name='update')),
                c.Heading(text=" ", level=2),
                c.Table(
                    data=data,
                    data_model=SportModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/sport/{id}/')),
                        DisplayLookup(field='sport_name'),
                    ],
                    no_data_message="Виды спорта отсутствуют"
                ),
                c.Button(text="Добавить спорт", on_click=GoToEvent(url="/sport/add")),
            ]
        ),
    ]

@router.get("/api/sport/{id}/", response_model=FastUI, response_model_exclude_none=True)
def sport_profile(id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    sport = get_object_by_id(db, id, SportModel, SportsOrm)
    return [
        c.Page(
            components=[
                c.Heading(text=sport.sport_name, level=2),
                c.Button(text="Назад", on_click=BackEvent()),
                c.Details(data=sport),
                c.Button(text="Редактировать вид спорта", on_click=GoToEvent(url=f"/sport/{id}/update")),
                c.Text(text="   "),
                c.Button(text="Удалить спорт", on_click=PageEvent(name="delete-sport")),
                c.Form(
                    submit_url="/api/sports/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-sport"),
                ),
            ]
        ),
    ]


@router.post("/api/sports/update/{id}")
def update_sport(
        id: int,
        form: Annotated[SportCreate, fastui_form(SportCreate)],
        db: Session = Depends(get_db)
):
    update_object_by_id(db, id, form, SportsOrm)
    return [c.FireEvent(event=GoToEvent(url=f"/sport/{id}/"))]


@router.get("/api/sport/{id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_sport_page(id: int, db: Session = Depends(get_db)):
    res = get_object_by_id(db, id, SportModel, SportsOrm)

    class SportUpdate(BaseModel):
        sport_name: str = Field(title="Название", default=res.sport_name)
        category: str = Field(title="Категория", default=res.category)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url=f"/sport/{id}/")),
                c.Heading(text='Редактировать вид спорта', level=2),
                c.ModelForm(
                    model=SportUpdate,
                    submit_url=f"/api/sports/update/{id}",
                )
            ]
        )
    ]

@router.post("/api/sports/delete")
def delete_sport(sport: Annotated[SportDelete, fastui_form(SportDelete)], db: Session = Depends(get_db)):
    delete_object_by_id(db, sport.id, SportsOrm)
    return [c.FireEvent(event=GoToEvent(url="/sports"))]