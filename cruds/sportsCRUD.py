from sqlalchemy import select, desc, text
from sqlalchemy.orm import Session
from orm.sports_orm import SportsOrm
from schemas.sports_schemas import SportModel, SportsFieldsDict


def get_sports_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str,
        search: str | None
):
    query = """
            SELECT * FROM sports
        """

    if search:
        if search_field == "Категория" and search in ["winter", "summer"]:
            query += f"""
                    WHERE {SportsFieldsDict[search_field]} = '{search}'
                """
        elif search_field != "Сезон":
            query += f"""
                    WHERE {SportsFieldsDict[search_field]} LIKE '{search}%'
                """

    query += f"""
            ORDER BY {SportsFieldsDict[sort_field]}
        """

    if reverse == "По убыванию":
        query += """ DESC"""

    result = [SportModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    return result
