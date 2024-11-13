from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas.countries_schemas import CountryModel, CountriesFieldsDict, CountryAndCount


def get_countries_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str,
        search: str | None
):
    query = """
            SELECT * FROM countries
        """

    if search:
        query += f"""
                WHERE {CountriesFieldsDict[search_field]} LIKE '{search}%'
            """

    query += f"""
            ORDER BY {CountriesFieldsDict[sort_field]}
        """

    if reverse == "По убыванию":
        query += """ DESC"""

    result = [CountryModel.model_validate(row, from_attributes=True) for row in db.execute(text(query)).all()]

    return result

def get_eurasia_countries(
        db: Session
):
    query = text("SELECT * from eurasia_countries")
    return [CountryModel(id=row[0], country_name=row[1], continent=row[2]) for row in db.execute(query).all()]

def get_athletes_count(
        db: Session
):
    query = text("SELECT * FROM athletes_by_country")
    return [CountryAndCount(country_name=row[0], count=row[1]) for row in db.execute(query).all()]