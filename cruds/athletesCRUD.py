from sqlalchemy import desc, select, text
from sqlalchemy.orm import Session
from orm.athletes_orm import AthletesOrm
from schemas.athletes_schemas import AthleteModel, AthletesFieldsDict, AthleteCreateToCountry
from schemas.schemas import GenderType


def get_athletes_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str,
        search: str | None
):
    query = """
        SELECT * FROM athletes
    """

    if search:
        query += f"""
            WHERE {AthletesFieldsDict[search_field]} LIKE '{search}%'
        """

    query += f"""
        ORDER BY {AthletesFieldsDict[sort_field]}
    """

    if reverse == "По убыванию":
        query += """ DESC"""

    result = [AthleteModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    return result

def create_athlete_to_country(id: int, form: AthleteCreateToCountry, db: Session):
    fields = form.model_dump()
    fields.update(dict(country_id=str(id)))
    db_athlete = AthletesOrm(**fields)
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)