from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from cruds.countriesCRUD import get_all_countries_list, get_country_by_id, delete_country_by_id, create_country, \
    get_sorted_countries_list
from routers.athlete_router import SortTypeForm
from schemas.schemas import CountryDelete, CountryCreate, CountryModel, CountriesFields, SortType
from database import get_db

router = APIRouter()

class SortForm(BaseModel):
    field: CountriesFields

@router.get("/api/countries", response_model=FastUI, response_model_exclude_none=True)
def countries_table(db: Session = Depends(get_db), field: CountriesFields | None = CountriesFields.country_name, reverse: SortType = SortType.false) -> list[AnyComponent]:
    data = get_all_countries_list(db)
    if field:
        if reverse == reverse.false:
            data = get_sorted_countries_list(db, field)
        else:
            data = get_sorted_countries_list(db, field, True)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='Страны', level=2),
                c.ModelForm(
                    model=SortTypeForm,
                    submit_url=".",
                    submit_on_change=True,
                    method="GOTO",
                    display_mode='inline',
                ),
                c.ModelForm(
                    model=SortForm,
                    submit_url=".",
                    submit_on_change=True,
                    method="GOTO",
                    display_mode='inline',
                ),
                c.Table(
                    data=data,
                    data_model=CountryModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/country/{id}/')),
                        DisplayLookup(field='country_name'),
                        DisplayLookup(field='continent'),
                    ],
                ),
                c.Button(text="Добавить страну", on_click=GoToEvent(url="/country/add")),
            ]
        ),
    ]

@router.get("/api/country/{country_id}/", response_model=FastUI, response_model_exclude_none=True)
def country_profile(country_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    country = get_country_by_id(db, country_id)
    return [
        c.Page(
            components=[
                c.Heading(text=country.country_name, level=2),
                c.Button(text="Назад", on_click=BackEvent()),
                c.Details(data=country),
                c.Button(text="Удалить страну", on_click=PageEvent(name="delete-country")),
                c.Form(
                    submit_url="/api/countries/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=country_id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-country"),
                ),
            ]
        ),
    ]

@router.post("/api/countries/delete")
def delete_country(country: Annotated[CountryDelete, fastui_form(CountryDelete)], db: Session = Depends(get_db)):
    delete_country_by_id(db, country.id)
    return [c.FireEvent(event=GoToEvent(url="/countries"))]

@router.get("/api/country/add", response_model=FastUI, response_model_exclude_none=True)
def add_athlete_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить страну', level=2),
                c.ModelForm(
                    model=CountryCreate,
                    submit_url="/api/country"
                )
            ]
        )
    ]

@router.post("/api/country")
def add_country(form: Annotated[CountryCreate, fastui_form(CountryCreate)], db: Session = Depends(get_db)):
    create_country(db, form)
    return [c.FireEvent(event=GoToEvent(url='/countries'))]