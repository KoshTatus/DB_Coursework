import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from cruds.eventsCRUD import get_events_list
from orm.events_orm import EventsOrm
from schemas.events_schemas import EventModel, EventCreate, SortFormEvent, EventDelete
from database import get_db
from cruds.generalCRUD import (
    get_all_objects,
    get_object_by_id,
    delete_object_by_id,
    update_object_by_id,
    create_object
)

router = APIRouter()


@router.post("/api/event")
def add_event(form: Annotated[EventCreate, fastui_form(EventCreate)], db: Session = Depends(get_db)):
    create_object(db, form, EventsOrm)
    return [c.FireEvent(event=GoToEvent(url='/events'))]

@router.get("/api/event/add", response_model=FastUI, response_model_exclude_none=True)
def add_event_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить событие', level=2),
                c.ModelForm(
                    model=EventCreate,
                    submit_url="/api/event"
                )
            ]
        )
    ]


@router.post("/api/events/sorting", response_model=FastUI, response_model_exclude_none=True)
def sort_events(
        form: Annotated[SortFormEvent, fastui_form(SortFormEvent)],
        db: Session = Depends(get_db)
):
    data = get_events_list(
        db,
        **form.model_dump()
    )
    return [
        c.Page(
            components=[
                c.Heading(text="Результат фильтра/сортировки", level=3),
                c.Table(
                    data=data,
                    data_model=EventModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/event/{id}/')),
                        DisplayLookup(field='event_name'),
                        DisplayLookup(field='sport_id', on_click=GoToEvent(url='/sport/{sport_id}/')),
                        DisplayLookup(field='olympic_id', on_click=GoToEvent(url='/olympic/{olympic_id}/')),
                    ],
                    no_data_message="Нет данных по этим параметрам"
                ),
            ]
        )
    ]

@router.get("/api/events", response_model=FastUI, response_model_exclude_none=True)
def events_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
    data = get_all_objects(db, EventModel, EventsOrm)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='События', level=2),
                c.ModelForm(
                    model=SortFormEvent,
                    submit_url="api/events/sorting",
                    display_mode="inline",
                    method="POST",
                    submit_on_change=False,
                    submit_trigger=PageEvent(name='update'),
                ),
                c.Button(text="Подтвердить", on_click=PageEvent(name='update')),
                c.Heading(text=" ", level=2),
                c.Table(
                    data=data,
                    data_model=EventModel,
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/event/{id}/')),
                        DisplayLookup(field='event_name'),
                        DisplayLookup(field='sport_id', on_click=GoToEvent(url='/sport/{sport_id}/')),
                        DisplayLookup(field='olympic_id', on_click=GoToEvent(url='/olympic/{olympic_id}/')),
                    ],
                    no_data_message="Нет событий"
                ),
                c.Button(text="Добавить событие", on_click=GoToEvent(url="/event/add")),
            ]
        ),
    ]

@router.get("/api/event/{id}/", response_model=FastUI, response_model_exclude_none=True)
def event_profile(id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    event = get_object_by_id(db, id, EventModel, EventsOrm)
    return [
        c.Page(
            components=[
                c.Heading(text=event.event_name, level=2),
                c.Button(text="Назад", on_click=BackEvent()),
                c.Details(data=event),
                c.Button(text="Редактировать событие", on_click=GoToEvent(url=f"/event/{id}/update")),
                c.Text(text="   "),
                c.Button(text="Удалить событие", on_click=PageEvent(name="delete-event")),
                c.Form(
                    submit_url="/api/events/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-event"),
                ),
            ]
        ),
    ]


@router.post("/api/events/update/{id}")
def update_event(
        id: int,
        form: Annotated[EventCreate, fastui_form(EventCreate)],
        db: Session = Depends(get_db)
):
    update_object_by_id(db, id, form, EventsOrm)
    return [c.FireEvent(event=GoToEvent(url=f"/event/{id}/"))]


@router.get("/api/event/{id}/update", response_model=FastUI, response_model_exclude_none=True)
def update_event_page(id: int, db: Session = Depends(get_db)):
    res = get_object_by_id(db, id, EventModel, EventsOrm)

    class EventUpdate(BaseModel):
        event_name: str = Field(title="Название", default=res.event_name)
        sport_id: int = Field(title="ID вида спорта", default=res.sport_id)
        event_date: datetime.date = Field(title="Дата", default=res.event_date)
        olympic_id: int = Field(title="ID олимпиады", default=res.olympic_id)

    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url=f"/event/{id}/")),
                c.Heading(text='Редактировать событие', level=2),
                c.ModelForm(
                    model=EventUpdate,
                    submit_url=f"/api/events/update/{id}",
                )
            ]
        )
    ]

@router.post("/api/events/delete")
def delete_event(event: Annotated[EventDelete, fastui_form(EventDelete)], db: Session = Depends(get_db)):
    delete_object_by_id(db, event.id, EventsOrm)
    return [c.FireEvent(event=GoToEvent(url="/events"))]



