from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.olympics_schemas import OlympicsFieldsDict, OlympicModel


def get_olympics_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str | None,
        search: str | None
):
    query = """
            SELECT * FROM olympics
        """

    if search:
        if search_field == "Сезон" and search in ["winter", "summer"]:
            query += f"""
                    WHERE {OlympicsFieldsDict[search_field]} = '{search}'
                """
        elif search_field != "Сезон":
            query += f"""
                    WHERE {OlympicsFieldsDict[search_field]} LIKE '{search}%'
                """

    query += f"""
            ORDER BY {OlympicsFieldsDict[sort_field]}
        """

    if reverse == "По убыванию":
        query += """ DESC"""

    result = [OlympicModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    return result