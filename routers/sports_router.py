from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from sqlalchemy.orm import Session
from cruds.sportsCRUD import get_sport_by_id, get_sport_by_name, get_all_sports, get_all_sports_list, delete_sport_by_id, create_sport
from schemas.schemas import SportCreate, SportDelete, SportModel
from database import get_db

router = APIRouter()

@router.get("/api/sports", response_model=FastUI, response_model_exclude_none=True)
def sports_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Виды спорта', level=2),
                c.Table(
                    data=get_all_sports_list(db),
                    data_model=SportModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/sport/{id}/')),
                        DisplayLookup(field='sport_name'),
                        DisplayLookup(field='category'),
                    ],
                ),
                c.Button(text="Добавить вид спорта", on_click=GoToEvent(url="/sport/add")),
            ]
        ),
    ]

@router.get("/api/sport/{sport_id}/", response_model=FastUI, response_model_exclude_none=True)
def sport_profile(sport_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    sport = get_sport_by_id(db, sport_id)
    return [
        c.Page(
            components=[
                c.Heading(text=sport.sport_name, level=2),
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Details(data=sport),
                c.Button(text="Удалить вид спорта", on_click=PageEvent(name="delete-sport")),
                c.Form(
                    submit_url="/api/sports/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=sport_id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-sport"),
                ),
            ]
        ),
    ]

@router.post("/api/sports/delete")
def delete_country(sport: Annotated[SportDelete, fastui_form(SportDelete)], db: Session = Depends(get_db)):
    delete_sport_by_id(db, sport.id)
    return [c.FireEvent(event=GoToEvent(url="/sports"))]

@router.get("/api/sport/add", response_model=FastUI, response_model_exclude_none=True)
def add_country_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить вид спорта', level=2),
                c.ModelForm(
                    model=SportCreate,
                    submit_url="/api/sport"
                )
            ]
        )
    ]

@router.post("/api/sport")
def add_sport(form: Annotated[SportCreate, fastui_form(SportCreate)], db: Session = Depends(get_db)):
    create_sport(db, form)
    return [c.FireEvent(event=GoToEvent(url='/sports'))]