from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from orm.orm import EventsOrm, CountriesOrm, OlympicsOrm, SportsOrm
from schemas.events_schemas import EventModel, EventCreate, EventsFieldsDict
from schemas.schemas import GenderType


def create_event(db: Session, event: EventCreate):
    if len(db.query(OlympicsOrm).filter(OlympicsOrm.id == event.olympic_id).all()) < 1:
        raise HTTPException(status_code=400, detail="Invalid olympic id!")
    if len(db.query(SportsOrm).filter(SportsOrm.id == event.sport_id).all()) < 1:
        raise HTTPException(status_code=400, detail="Invalid sport id!")
    db_event = EventsOrm(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)


def get_events_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search: str | None
):
    query = select(EventsOrm)

    if search:
        if reverse == "По возрастанию":
            query = select(EventsOrm).filter(EventsOrm.event_name.like(f"{search}%")).order_by(
                    EventsFieldsDict[sort_field])
        else:
            query = select(EventsOrm).filter(EventsOrm.event_name.like(f"{search}%")).order_by(
                    desc(EventsFieldsDict[sort_field]))
    else:
        if reverse == "По возрастанию":
            query = select(EventsOrm).order_by(EventsFieldsDict[sort_field])
        else:
            query = select(EventsOrm).order_by(desc(EventsFieldsDict[sort_field]))

    result = [EventModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result


def get_all_events(db: Session):
    query = select(EventsOrm)
    res = db.execute(query)
    ans = [EventModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans


def get_event_by_id(db: Session, id: int):
    result = db.query(EventsOrm).filter(EventsOrm.id == id).all()
    return EventModel.model_validate(result[0], from_attributes=True)


def update_event_by_id(db: Session, id: int, new_fields: EventCreate):
    if len(db.query(OlympicsOrm).filter(OlympicsOrm.id == new_fields.olympic_id).all()) < 1:
        raise HTTPException(status_code=400, detail="Invalid olympic id!")
    if len(db.query(SportsOrm).filter(SportsOrm.id == new_fields.sport_id).all()) < 1:
        raise HTTPException(status_code=400, detail="Invalid sport id!")

    db.query(EventsOrm).filter(EventsOrm.id == id).update(new_fields.model_dump())
    db.commit()


def delete_event_by_id(db: Session, id: int):
    db.query(EventsOrm).filter(EventsOrm.id == id).delete()
    db.commit()
