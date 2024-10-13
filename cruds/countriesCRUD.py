from fastapi import Query, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.orm import CountriesOrm
from schemas.countries_schemas import CountryModel, CountryCreate, CountryUpdate, CountriesFields

SKIP = 0
LIMIT = 20

def get_sorted_countries_list(db: Session, field: CountriesFields = CountriesFields.country_name, reverse: bool = False, skip: int = SKIP, limit: int = LIMIT):
    if reverse:
        query = select(CountriesOrm).order_by(desc(field.value))
    else:
        query = select(CountriesOrm).order_by(field.value)

    result = [CountryModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result

def get_all_countries(db: Session, skip: int = SKIP, limit: int = LIMIT):
    return db.query(CountriesOrm).offset(skip).limit(limit).all()

def get_country_by_name(db: Session, country_name):
    return db.query(CountriesOrm).filter(CountriesOrm.country_name == country_name).first()

def create_country(db: Session, country: CountryCreate):
    db_country = CountriesOrm(**country.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_country_by_id(db: Session, id: int):
    result = db.query(CountriesOrm).filter(CountriesOrm.id == id).all()
    if len(result) < 1:
        raise HTTPException(status_code=404, detail="The athlete with this ID does not exist!")
    return CountryModel.model_validate(result[0], from_attributes=True)

def get_all_countries_list(db: Session, skip: int = SKIP, limit: int = LIMIT):
    query = (select(CountriesOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [CountryModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans

def update_country_by_id(db: Session, new_country: CountryUpdate):
    if len(db.query(CountriesOrm).filter(CountriesOrm.id == new_country.id).all()) < 1:
        raise HTTPException(status_code=404, detail="The country with the ID data does not exist!")

    return db.query(CountriesOrm).filter(CountriesOrm.id == new_country.id).first()

def delete_country_by_id(db: Session, id: int):
    deleted = db.query(CountriesOrm).filter(CountriesOrm.id == id).first()
    db.query(CountriesOrm).filter(CountriesOrm.id == id).delete()
    db.commit()

    return deleted
