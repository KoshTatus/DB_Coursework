from fastapi import Query, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.orm import EventsOrm
from schemas.events_schemas import EventModel, EventCreate, EventsFields

SKIP = 0
LIMIT = 20


def get_sorted_events_list(db: Session, field: EventsFields = EventsFields.event_name, reverse: bool = False, skip: int = SKIP, limit: int = LIMIT):
    if reverse:
        query = select(EventsOrm).order_by(desc(field.value))
    else:
        query = select(EventsOrm).order_by(field.value)

    result = [EventModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result

def get_all_events(db: Session, skip: int = SKIP, limit: int = LIMIT):
    return db.query(EventsOrm).offset(skip).limit(limit).all()

def get_event_by_name(db: Session, event_name):
    return db.query(EventsOrm).filter(EventsOrm.event_name == event_name).first()

def create_event(db: Session, event: EventCreate):
    db_event = EventsOrm(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event_by_id(db: Session, id: int):
    result = db.query(EventsOrm).filter(EventsOrm.id == id).all()
    if len(result) < 1:
        raise HTTPException(status_code=404, detail="The athlete with this ID does not exist!")
    return EventModel.model_validate(result[0], from_attributes=True)

def get_all_events_list(db: Session, skip: int = SKIP, limit: int = LIMIT):
    query = (select(EventsOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [EventModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans

def update_country_by_id(db: Session, new_event: EventCreate):
    if len(db.query(EventsOrm).filter(EventsOrm.id == new_event.id).all()) < 1:
        raise HTTPException(status_code=404, detail="The country with the ID data does not exist!")

    return db.query(EventsOrm).filter(EventsOrm.id == new_event.id).first()

def delete_athlete_by_id(db: Session, id: int):
    deleted = db.query(EventsOrm).filter(EventsOrm.id == id).first()
    db.query(EventsOrm).filter(EventsOrm.id == id).delete()
    db.commit()

    return deleted
