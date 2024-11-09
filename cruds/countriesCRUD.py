from sqlalchemy import select, desc, text
from sqlalchemy.orm import Session
from orm.countries_orm import CountriesOrm
from schemas.countries_schemas import CountryModel, CountriesFieldsDict, CountryAndCount


def get_countries_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str,
        search: str | None
):
    query = select(CountriesOrm)

    if search:
        match search_field:
            case "Название":
                if reverse == "По возрастанию":
                    query = select(CountriesOrm).filter(CountriesOrm.country_name.like(f"{search}%")).order_by(
                        CountriesFieldsDict[sort_field])
                else:
                    query = select(CountriesOrm).filter(CountriesOrm.continent.like(f"{search}%")).order_by(
                        desc(CountriesFieldsDict[sort_field]))
            case "Континент":
                if reverse == "По возрастанию":
                    query = select(CountriesOrm).filter(CountriesOrm.country_name.like(f"{search}%")).order_by(
                        CountriesFieldsDict[sort_field])
                else:
                    query = select(CountriesOrm).filter(CountriesOrm.continent.like(f"{search}%")).order_by(
                        desc(CountriesFieldsDict[sort_field]))
    else:
        if reverse == "По возрастанию":
            query = select(CountriesOrm).order_by(CountriesFieldsDict[sort_field])
        else:
            query = select(CountriesOrm).order_by(desc(CountriesFieldsDict[sort_field]))

    result = [CountryModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

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