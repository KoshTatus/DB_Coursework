from typing import Annotated
from fastapi import APIRouter, Depends
from fastui import components as c, AnyComponent, FastUI
from fastui.events import GoToEvent, BackEvent
from fastui.forms import fastui_form
from sqlalchemy.orm import Session
from database.database import get_db
from reports.reports import first_report, second_report, third_report
from schemas.reports_schemas import FirstReportFields, SecondReportFields, ThirdReportFields

router = APIRouter(
    prefix="/api/reports"
)


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def reports_page() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/")),
                c.Heading(text="Отчеты"),
                c.Button(
                    text="Количество атлетов на олимпиаде по странам",
                    on_click=GoToEvent(url="/reports/1")
                ),
                c.Heading(text=" "),
                c.Button(
                    text="Количество событий по каждому виду спорта на олимпиалдах",
                    on_click=GoToEvent(url="/reports/2")
                ),
                c.Heading(text=" "),
                c.Button(
                    text="Количество медалей каждого атлета",
                    on_click=GoToEvent(url="/reports/3")
                ),
            ]
        )
    ]


@router.get("/1", response_model=FastUI, response_model_exclude_none=True)
def first_report_page() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/reports")),
                c.Heading(text=" "),
                c.Heading(text="Выберите параметры"),
                c.ModelForm(
                    model=FirstReportFields,
                    submit_url=f"/api/reports/1/download",
                    method="POST",
                    submit_on_change=False,
                ),
            ]
        )
    ]


@router.get("/2", response_model=FastUI, response_model_exclude_none=True)
def second_report_page() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/reports")),
                c.Heading(text=" "),
                c.Heading(text="Выберите параметры"),
                c.ModelForm(
                    model=SecondReportFields,
                    submit_url=f"/api/reports/2/download",
                    method="POST",
                    submit_on_change=False,
                ),
            ]
        )
    ]

@router.get("/3", response_model=FastUI, response_model_exclude_none=True)
def third_report_page() -> list[AnyComponent]:
    return [
        c.Page(
            components=[
                c.Button(text="Назад", on_click=GoToEvent(url="/reports")),
                c.Heading(text=" "),
                c.Heading(text="Выберите параметры"),
                c.ModelForm(
                    model=ThirdReportFields,
                    submit_url=f"/api/reports/3/download",
                    method="POST",
                    submit_on_change=False,
                ),
            ]
        )
    ]


@router.post("/1/download", response_model=FastUI, response_model_exclude_none=True)
def save_first_report(
        form: Annotated[FirstReportFields, fastui_form(FirstReportFields)],
        db: Session = Depends(get_db)
):
    first_report(db, form)
    return [
        c.Page(
            components=[
                c.Heading(text=""),
                c.Text(
                    text=f"Отчет report_1.txt был сохранен в "
                         f"C:/Users/Егор/Desktop/Курсовая_БД/reports/report_files/report_1.txt ")
            ]
        )
    ]

@router.post("/2/download", response_model=FastUI, response_model_exclude_none=True)
def save_second_report(
        form: Annotated[SecondReportFields, fastui_form(SecondReportFields)],
        db: Session = Depends(get_db)
):
    second_report(db, form)
    return [
        c.Page(
            components=[
                c.Heading(text=""),
                c.Text(
                    text=f"Отчет report_2.txt был сохранен в "
                         f"C:/Users/Егор/Desktop/Курсовая_БД/reports/report_files/report_2.txt ")
            ]
        )
    ]

@router.post("/3/download", response_model=FastUI, response_model_exclude_none=True)
def save_third_report(
        form: Annotated[ThirdReportFields, fastui_form(ThirdReportFields)],
        db: Session = Depends(get_db)
):
    third_report(db, form)
    return [
        c.Page(
            components=[
                c.Heading(text=""),
                c.Text(
                    text=f"Отчет report_3.txt был сохранен в "
                         f"C:/Users/Егор/Desktop/Курсовая_БД/reports/report_files/report_3.txt ")
            ]
        )
    ]