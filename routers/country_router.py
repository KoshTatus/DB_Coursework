from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from cruds.countriesCRUD import get_countries_list, get_eurasia_countries, get_athletes_count
from orm.countries_orm import CountriesOrm
from schemas.countries_schemas import CountryDelete, CountryCreate, CountryModel, SortFormCountry, \
    CountryAndCount
from database.database import get_db
from cruds.generalCRUD import (
    get_all_objects,
    get_object_by_id,
    delete_object_by_id,
    update_object_by_id,
    create_object
)
router = APIRouter(
    prefix="/api"
)

@router.post("/country")
def add_country(form: Annotated[CountryCreate, fastui_form(CountryCreate)], db: Session = Depends(get_db)):
    create_object(db, form, CountriesOrm)
    return [c.FireEvent(event=GoToEvent(url='/countries'))]

@router.get("/country/add", response_model=FastUI, response_model_exclude_none=True)
def add_country_page():
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


@router.post("/countries/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_countries(
        form: Annotated[SortFormCountry, fastui_form(SortFormCountry)],
        db: Session = Depends(get_db)
):
    data = get_countries_list(
        db,
        **form.model_dump()
    )
    return [
        c.Page(
            components=[
                c.Heading(text="Результат фильтра/сортировки", level=3),
                c.Table(
                    data=data,
                    data_model=CountryModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/country/{id}/')),
                        DisplayLookup(field='country_name'),
                        DisplayLookup(field='continent'),
                    ],
                    no_data_message="Нет данных по этим параметрам"
                ),
            ]
        )
    ]

@router.get("/countries/view/1", response_model=FastUI, response_model_exclude_none=True)
def eurasia_country(db: Session = Depends(get_db)) -> list[AnyComponent]:
    data = get_eurasia_countries(db)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Страны Евразии', level=2),
                c.Table(
                    data=data,
                    data_model=CountryModel,
                    columns=[
                        DisplayLookup(field='country_name')
                    ]
                )
            ]
        )
    ]

@router.get("/countries/view/2", response_model=FastUI, response_model_exclude_none=True)
def athletes_count(db: Session = Depends(get_db)):
    data = get_athletes_count(db)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Количество атлетов по странам', level=2),
                c.Table(
                    data=data,
                    data_model=CountryAndCount,
                    columns=[
                        DisplayLookup(field='country_name'),
                        DisplayLookup(field='count')
                    ]
                )
            ]
        )
    ]

@router.get("/countries", response_model=FastUI, response_model_exclude_none=True)
def countries_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    data = get_all_objects(db, CountryModel, CountriesOrm)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Text(text=" "),
                c.Button(text="Страны Евразии", on_click=GoToEvent(url="/countries/view/1")),
                c.Text(text=" "),
                c.Button(text="Количество атлетов по странам", on_click=GoToEvent(url="/countries/view/2")),
                c.Heading(text='Страны', level=2),
                c.ModelForm(
                    model=SortFormCountry,
                    submit_url="api/countries/sorting",
                    display_mode="inline",
                    method="POST",
                    submit_on_change=False,
                    submit_trigger=PageEvent(name='update'),
                ),
                c.Button(text="Подтвердить", on_click=PageEvent(name='update')),
                c.Heading(text=" ", level=2),
                c.Table(
                    data=data,
                    data_model=CountryModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/country/{id}/'), title='ID'),
                        DisplayLookup(field='country_name'),
                        DisplayLookup(field='continent'),
                    ],
                    no_data_message="Страны отсутсвуют"
                ),
                c.Button(text="Добавить страну", on_click=GoToEvent(url="/country/add")),
            ]
        ),
    ]

@router.get("/country/{id}/", response_model=FastUI, response_model_exclude_none=True)
def country_profile(id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    country = get_object_by_id(db, id, CountryModel, CountriesOrm)
    return [
        c.Page(
            components=[
                c.Heading(text=country.country_name, level=2),
                c.Button(text="Назад", on_click=GoToEvent(url=f"/countries")),
                c.Details(data=country),
                c.Button(text="Редактировать страну", on_click=GoToEvent(url=f"/country/{id}/update")),
                c.Text(text="   "),
                c.Button(text="Удалить страну", on_click=PageEvent(name="delete-country")),
                c.Text(text="   "),
                c.Button(text="Добавить атлета к стране", on_click=GoToEvent(url=f"/add_to_country/{id}")),
                c.Form(
                    submit_url="/api/countries/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-country"),
                ),
            ]
        ),
    ]


@router.post("/countries/update/{id}")
def update_athlete(id: int, form: Annotated[CountryCreate, fastui_form(CountryCreate)],
                   db: Session = Depends(get_db)):
    update_object_by_id(db, id, form, CountriesOrm)
    return [c.FireEvent(event=GoToEvent(url=f"/country/{id}/"))]


@router.get("/country/{id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_country_page(id: int, db: Session = Depends(get_db)):
    res = get_object_by_id(db, id, CountryModel, CountriesOrm)

    class CountryUpdate(BaseModel):
        country_name: str = Field(title="Название", default=res.country_name)
        continent: str = Field(title="Континент", default=res.continent)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url=f"/country/{id}/")),
                c.Heading(text='Редактировать страну', level=2),
                c.ModelForm(
                    model=CountryUpdate,
                    submit_url=f"/countries/update/{id}",
                )
            ]
        )
    ]

@router.post("/countries/delete")
def delete_country(country: Annotated[CountryDelete, fastui_form(CountryDelete)], db: Session = Depends(get_db)):
    delete_object_by_id(db, country.id, CountriesOrm)
    return [c.FireEvent(event=GoToEvent(url="/countries"))]



