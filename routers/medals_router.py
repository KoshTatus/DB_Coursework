from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from cruds.medalsCRUD import get_medals_list
from orm.medals_orm import MedalsOrm
from schemas.medals_schemas import MedalCreate, MedalDelete, MedalModel, SortFormMedal
from database import get_db
from cruds.generalCRUD import (
    get_all_objects,
    get_object_by_id,
    delete_object_by_id,
    update_object_by_id,
    create_object
)

router = APIRouter()


@router.post("/api/medal")
def add_medal(form: Annotated[MedalCreate, fastui_form(MedalCreate)], db: Session = Depends(get_db)):
    create_object(db, form, MedalsOrm)
    return [c.FireEvent(event=GoToEvent(url='/medals'))]

@router.get("/api/medal/add", response_model=FastUI, response_model_exclude_none=True)
def add_medal_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить медаль', level=2),
                c.ModelForm(
                    model=MedalCreate,
                    submit_url="/api/medal"
                )
            ]
        )
    ]


@router.post("/api/medals/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_medals(
        form: Annotated[SortFormMedal, fastui_form(SortFormMedal)],
        db: Session = Depends(get_db)
):
    data = get_medals_list(
        db,
        **form.model_dump()
    )
    return [
        c.Page(
            components=[
                c.Heading(text="Результат фильтра/сортировки", level=3),
                c.Table(
                    data=data,
                    data_model=MedalModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/medal/{id}/')),
                        DisplayLookup(field='event_id', on_click=GoToEvent(url='/event/{event_id}/')),
                        DisplayLookup(field='athlete_id', on_click=GoToEvent(url='/athlete/{athlete_id}/')),
                        DisplayLookup(field='medal_type')
                    ],
                    no_data_message="Нет данных по этим параметрам"
                ),
            ]
        )
    ]


@router.get("/api/medals", response_model=FastUI, response_model_exclude_none=True)
def medals_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    data = get_all_objects(db, MedalModel, MedalsOrm)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='Медали', level=2),
                c.ModelForm(
                    model=SortFormMedal,
                    submit_url="api/medals/sorting",
                    display_mode="inline",
                    method="POST",
                    submit_on_change=False,
                    submit_trigger=PageEvent(name='update'),
                ),
                c.Button(text="Подтвердить", on_click=PageEvent(name='update')),
                c.Heading(text=" ", level=2),
                c.Table(
                    data=data,
                    data_model=MedalModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/medal/{id}/')),
                        DisplayLookup(field='medal_type'),
                    ],
                ),
                c.Button(text="Добавить медаль", on_click=GoToEvent(url="/medal/add")),
            ]
        ),
    ]

@router.get("/api/medal/{id}/", response_model=FastUI, response_model_exclude_none=True)
def medal_profile(id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    medal = get_object_by_id(db, id, MedalModel, MedalsOrm)
    return [
        c.Page(
            components=[
                c.Heading(text=str(medal.id), level=2),
                c.Button(text="Назад", on_click=BackEvent()),
                c.Details(data=medal),
                c.Button(text="Удалить медаль", on_click=PageEvent(name="delete-medal")),
                c.Form(
                    submit_url="/api/medals/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-medal"),
                ),
            ]
        ),
    ]

@router.post("/api/medals/update/{id}")
def update_medal(
        id: int,
        form: Annotated[MedalCreate, fastui_form(MedalCreate)],
        db: Session = Depends(get_db)
):
    update_object_by_id(db, id, form, MedalsOrm)
    return [c.FireEvent(medal=GoToEvent(url=f"/medal/{id}/"))]


@router.get("/api/medal/{id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_medal_page(id: int, db: Session = Depends(get_db)):
    res = get_object_by_id(db, id, MedalModel, MedalsOrm)

    class MedalUpdate(BaseModel):
        event_id: int = Field(title="ID вида спорта", default=res.sport_id)
        athlete_id: int = Field(title="ID атлета", default=res.athlete_id)
        medal_type: str = Field(title="Тип медали", default=res.medal_type)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url=f"/medal/{id}/")),
                c.Heading(text='Редактировать событие', level=2),
                c.ModelForm(
                    model=MedalUpdate,
                    submit_url=f"/api/medals/update/{id}",
                )
            ]
        )
    ]

@router.post("/api/medals/delete")
def delete_medal(medal: Annotated[MedalDelete, fastui_form(MedalDelete)], db: Session = Depends(get_db)):
    delete_object_by_id(db, medal.id, MedalsOrm)
    return [c.FireEvent(event=GoToEvent(url="/medals"))]



