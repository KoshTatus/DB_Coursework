from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.countries_orm import CountriesOrm
from schemas.countries_schemas import CountryModel, CountriesFieldsDict


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