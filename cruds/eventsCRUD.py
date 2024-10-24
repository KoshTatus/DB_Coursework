from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from orm.events_orm import EventsOrm
from schemas.events_schemas import EventModel, EventsFieldsDict


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