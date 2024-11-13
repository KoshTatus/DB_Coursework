from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.medals_schemas import MedalModel, MedalsFieldsDict, MedalType


def get_medals_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: MedalType | None
):
    query = """
            SELECT * FROM medals
        """

    if search_field:
        query += f"""
                WHERE medals.medal_type = '{search_field.value}'
            """

    query += f"""
            ORDER BY {MedalsFieldsDict[sort_field]}
        """

    if reverse == "По убыванию":
        query += """ DESC"""

    result = [MedalModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    return result