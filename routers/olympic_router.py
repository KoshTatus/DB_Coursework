# from typing import Annotated
# from fastapi import APIRouter, Depends
# from fastui.components.display import DisplayLookup
# from fastui.events import GoToEvent, PageEvent, BackEvent
# from fastui.forms import fastui_form
# from fastui import components as c, AnyComponent, FastUI
# from sqlalchemy.orm import Session
#
# from cruds.olympicsCRUD import get_all_olympics_list, create_olympic, get_olympic_by_id, delete_olympic_by_id
# from schemas.olympics_schemas import OlympicModel, OlympicCreate, OlympicDelete
# from database import get_db
#
# router = APIRouter()
#
# @router.get("/api/olympics", response_model=FastUI, response_model_exclude_none=True)
# def olympics_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
#     return [
#         c.Page(
#             components=[
#                 c.Button(text="Назад", on_click=GoToEvent(url="/")),
#                 c.Heading(text='Олимпиады', level=2),
#                 c.Table(
#                     data=get_all_olympics_list(db),
#                     data_model=OlympicModel,
#                     columns=[
#                         DisplayLookup(field='id', on_click=GoToEvent(url='/olympic/{id}/')),
#                         DisplayLookup(field='location'),
#                     ],
#                 ),
#                 c.Button(text="Добавить олимпиаду", on_click=GoToEvent(url="/olympic/add")),
#             ]
#         ),
#     ]
#
# @router.get("/api/olympic/{olymic_id}/", response_model=FastUI, response_model_exclude_none=True)
# def olympic_profile(olymic_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
#     olymic = get_olympic_by_id(db, olymic_id)
#     return [
#         c.Page(
#             components=[
#                 c.Heading(text=olymic.location, level=2),
#                 c.Button(text="Назад", on_click=BackEvent()),
#                 c.Details(data=olymic),
#                 c.Button(text="Удалить олимпиаду", on_click=PageEvent(name="delete-olympic")),
#                 c.Form(
#                     submit_url="/api/olympics/delete",
#                     form_fields=[
#                         c.FormFieldInput(name='id', title='', initial=olymic_id, html_type='hidden')
#                     ],
#                     footer=[],
#                     submit_trigger=PageEvent(name="delete-olympic"),
#                 ),
#             ]
#         ),
#     ]
#
# @router.post("/api/olympics/delete")
# def delete_olympic(olympic: Annotated[OlympicDelete, fastui_form(OlympicDelete)], db: Session = Depends(get_db)):
#     delete_olympic_by_id(db, olympic.id)
#     return [c.FireEvent(event=GoToEvent(url="/olympics"))]
#
# @router.get("/api/olympic/add", response_model=FastUI, response_model_exclude_none=True)
# def add_olympic_page():
#     return [
#         c.Page(
#             components=[
#                 c.Button(text="Назад", on_click=BackEvent()),
#                 c.Heading(text='Добавить олимпиаду', level=2),
#                 c.ModelForm(
#                     model=OlympicCreate,
#                     submit_url="/api/olympic"
#                 )
#             ]
#         )
#     ]
#
# @router.post("/api/olympic")
# def add_olympic(form: Annotated[OlympicCreate, fastui_form(OlympicCreate)], db: Session = Depends(get_db)):
#     create_olympic(db, form)
#     return [c.FireEvent(event=GoToEvent(url='/olympics'))]