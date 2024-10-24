from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.events import GoToEvent

from statics.images import *

router = APIRouter()

@router.get("/api/", response_model=FastUI, response_model_exclude_none=True)
def show_tables() -> list[AnyComponent] :
    return [
        c.Page(
            components=[
                c.Heading(text="Таблицы", level=1),
                c.Button(text="Атлеты", on_click=GoToEvent(url="/athletes")),
                c.Image(src=athlete_url, height=100, width=100, on_click=GoToEvent(url="/athletes")),
                c.Text(text="   "),
                c.Button(text="Страны", on_click=GoToEvent(url="/countries")),
                c.Text(text="   "),
                c.Image(src=country_url, height=100, width=100, on_click=GoToEvent(url="/countries")),
                c.Text(text="   "),
                c.Button(text="События", on_click=GoToEvent(url="/events")),
                c.Text(text="   "),
                c.Image(src=events_url, height=100, width=100, on_click=GoToEvent(url="/events")),
                c.Text(text="   "),
                c.Button(text="Медали", on_click=GoToEvent(url="/medals")),
                c.Image(src=medal_url, height=100, width=100, on_click=GoToEvent(url="/medals")),
                c.Text(text="   "),
                c.Button(text="Виды спорта", on_click=GoToEvent(url="/sports")),
                c.Text(text="   "),
                c.Image(src=sport_url, height=100, width=100, on_click=GoToEvent(url="/sports")),
                c.Text(text="   "),
                c.Button(text="Олимпиады", on_click=GoToEvent(url="/olympics")),
                c.Text(text="   "),
                c.Image(src=olympics_url, height=100, width=130, on_click=GoToEvent(url="/olympics")),
                c.Text(text="   "),
            ]
        )
    ]

@router.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Olympic Database'))