from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.events_schemas import EventModel, EventsFieldsDict


def get_events_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search: str | None
):
    query = """
            SELECT * FROM events
        """

    if search:
        query += f"""
                WHERE {EventsFieldsDict['Название']} LIKE '{search}%'
            """

    query += f"""
            ORDER BY {EventsFieldsDict[sort_field]}
        """

    if reverse == "По убыванию":
        query += """ DESC"""

    result = [EventModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    return result