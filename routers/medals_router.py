# from typing import Annotated
# from fastapi import APIRouter, Depends
# from fastui.components.display import DisplayLookup
# from fastui.events import GoToEvent, PageEvent, BackEvent
# from fastui.forms import fastui_form
# from fastui import components as c, AnyComponent, FastUI
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from cruds.medalsCRUD import get_all_medals_list, get_medal_by_id, delete_medal_by_id, create_medal
# from schemas.medals_schemas import MedalCreate, MedalDelete, MedalModel
# from database import get_db
# from schemas.schemas import SortTypeForm, SortType
#
# router = APIRouter()
#
# @router.get("/api/medals", response_model=FastUI, response_model_exclude_none=True)
# def medals_table(db: Session = Depends(get_db)) -> list[AnyComponent]:
#     data = get_all_medals_list(db)
#     return [
#         c.Page(
#             components=[
#                 c.Button(text="Назад", on_click=GoToEvent(url="/")),
#                 c.Heading(text='Медали', level=2),
#                 c.ModelForm(
#                     model=SortTypeForm,
#                     submit_url=".",
#                     submit_on_change=True,
#                     method="GOTO",
#                     display_mode='inline',
#                 ),
#                 c.Table(
#                     data=data,
#                     data_model=MedalModel,
#                     columns=[
#                         DisplayLookup(field='id', on_click=GoToEvent(url='/medal/{id}/')),
#                         DisplayLookup(field='medal_type'),
#                     ],
#                 ),
#                 c.Button(text="Добавить медаль", on_click=GoToEvent(url="/medal/add")),
#             ]
#         ),
#     ]
#
# @router.get("/api/medal/{medal_id}/", response_model=FastUI, response_model_exclude_none=True)
# def medal_profile(medal_id: int, db: Session = Depends(get_db)) -> list[AnyComponent]:
#     medal = get_medal_by_id(db, medal_id)
#     return [
#         c.Page(
#             components=[
#                 c.Heading(text=str(medal.id), level=2),
#                 c.Button(text="Назад", on_click=BackEvent()),
#                 c.Details(data=medal),
#                 c.Button(text="Удалить медаль", on_click=PageEvent(name="delete-medal")),
#                 c.Form(
#                     submit_url="/api/medals/delete",
#                     form_fields=[
#                         c.FormFieldInput(name='id', title='', initial=medal_id, html_type='hidden')
#                     ],
#                     footer=[],
#                     submit_trigger=PageEvent(name="delete-medal"),
#                 ),
#             ]
#         ),
#     ]
#
# @router.post("/api/medals/delete")
# def delete_medal(medal: Annotated[MedalDelete, fastui_form(MedalDelete)], db: Session = Depends(get_db)):
#     delete_medal_by_id(db, medal.id)
#     return [c.FireEvent(event=GoToEvent(url="/medals"))]
#
# @router.get("/api/medal/add", response_model=FastUI, response_model_exclude_none=True)
# def add_medal_page():
#     return [
#         c.Page(
#             components=[
#                 c.Button(text="Назад", on_click=BackEvent()),
#                 c.Heading(text='Добавить медаль', level=2),
#                 c.ModelForm(
#                     model=MedalCreate,
#                     submit_url="/api/medal"
#                 )
#             ]
#         )
#     ]
#
# @router.post("/api/medal")
# def add_medal(form: Annotated[MedalCreate, fastui_form(MedalCreate)], db: Session = Depends(get_db)):
#     create_medal(db, form)
#     return [c.FireEvent(event=GoToEvent(url='/medals'))]