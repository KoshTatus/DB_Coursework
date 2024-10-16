from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.orm import CountriesOrm
from schemas.countries_schemas import CountryModel, CountryCreate, CountryUpdate, CountriesFieldsDict


def create_country(db: Session, country: CountryCreate):
    db_country = CountriesOrm(**country.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


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


def get_all_countries_list(db: Session):
    query = select(CountriesOrm)
    res = db.execute(query)
    ans = [CountryModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans


def get_country_by_id(db: Session, id: int):
    result = db.query(CountriesOrm).filter(CountriesOrm.id == id).all()
    return CountryModel.model_validate(result[0], from_attributes=True)

def update_country_by_id(db: Session, id: int, new_fields: CountryUpdate):
    db.query(CountriesOrm).filter(CountriesOrm.id == id).update(new_fields.model_dump())
    db.commit()

def delete_country_by_id(db: Session, id: int):
    db.query(CountriesOrm).filter(CountriesOrm.id == id).first()
    db.commit()