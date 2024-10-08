from typing import Annotated
from fastapi import APIRouter, Depends
from fastui.components.display import DisplayLookup
from fastui.events import GoToEvent, PageEvent, BackEvent
from fastui.forms import fastui_form
from fastui import components as c, AnyComponent, FastUI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from cruds.eventsCRUD import get_all_events_list, get_event_by_id, delete_athlete_by_id, create_event, \
    get_sorted_events_list
from schemas.schemas import EventDelete, EventCreate, EventModel, EventsFields, SortType, SortTypeForm
from database import get_db

router = APIRouter()

class SortForm(BaseModel):
    field: EventsFields

@router.post("/api/events/delete")
def delete_athlete(event: Annotated[EventDelete, fastui_form(EventDelete)], db: Session = Depends(get_db)):
    delete_athlete_by_id(db, event.id)
    return [c.FireEvent(event=GoToEvent(url="/events"))]

@router.post("/api/event")
def add_athlete(form: Annotated[EventCreate, fastui_form(EventCreate)], db: Session = Depends(get_db)):
    create_event(db, form)
    return [c.FireEvent(event=GoToEvent(url='/events'))]

@router.get("/api/event/{event_id}/", response_model=FastUI, response_model_exclude_none=True)
def athlete_profile(event_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
    event = get_event_by_id(db, event_id)
    return [
        c.Page(
            components=[
                c.Heading(text=event.event_name, level=2),
                c.Button(text="Назад", on_click=BackEvent()),
                c.Details(data=event),
                c.Button(text="Удалить событие", on_click=PageEvent(name="delete-event")),
                c.Form(
                    submit_url="/api/events/delete",
                    form_fields=[
                        c.FormFieldInput(name='id', title='', initial=event_id, html_type='hidden')
                    ],
                    footer=[],
                    submit_trigger=PageEvent(name="delete-event"),
                ),
            ]
        ),
    ]

@router.get("/api/events", response_model=FastUI, response_model_exclude_none=True)
def events_table(db: Session = Depends(get_db), field: EventsFields | None = EventsFields.event_name, reverse: SortType = SortType.false) -> list[AnyComponent]:
    data = get_all_events_list(db)
    if field:
        if reverse == reverse.false:
            data = get_sorted_events_list(db, field)
        else:
            data = get_sorted_events_list(db, field, True)
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text='События', level=2),
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
                    data_model=EventModel,
                    no_data_message="Нет событий",
                    columns=[
                        DisplayLookup(field='id', on_click=GoToEvent(url='/event/{id}/')),
                        DisplayLookup(field='event_name'),
                        DisplayLookup(field='sport_id'),
                        DisplayLookup(field='event_date'),
                        DisplayLookup(field='olympic_id'),
                    ],
                ),
                c.Button(text="Добавить событие", on_click=GoToEvent(url="/event/add")),
            ]
        ),
    ]

@router.get("/api/event/add", response_model=FastUI, response_model_exclude_none=True)
def add_event_page():
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=BackEvent()),
                c.Heading(text='Добавить событие', level=2),
                c.ModelForm(
                    model=EventCreate,
                    submit_url="/api/event",
                )
            ]
        )
    ]