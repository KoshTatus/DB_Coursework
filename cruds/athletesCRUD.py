import datetime
from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from orm.orm import AthletesOrm, CountriesOrm
from schemas.schemas import AthleteModel, AthleteCreate, AthletesFields, SortType

SKIP = 0
LIMIT = 20


def get_sorted_athletes_list(db: Session, field: AthletesFields = AthletesFields.last_name,
                             reverse: SortType = SortType.false, skip: int = SKIP, limit: int = LIMIT):
    if reverse.name == "true":
        query = select(AthletesOrm).order_by(desc(field.name))
    else:
        query = select(AthletesOrm).order_by(field.name)

    result = [AthleteModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result


def get_all_athletes(db: Session, skip: int = SKIP, limit: int = LIMIT):
    # res = db.query(AthletesOrm).offset(skip).limit(limit).all()
    query = (select(AthletesOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [AthleteModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return db.query(AthletesOrm).offset(skip).limit(limit).all()


def get_all_athletes_list(db: Session, skip: int = SKIP, limit: int = LIMIT):
    # res = db.query(AthletesOrm).offset(skip).limit(limit).all()
    query = (select(AthletesOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [AthleteModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans


def get_athlete_by_name(db: Session, first_name: str, last_name: str, skip: int = SKIP, limit: int = LIMIT):
    return db.query(AthletesOrm).filter(
        AthletesOrm.first_name == first_name and
        AthletesOrm.last_name == last_name).offset(skip).limit(limit).all()


def create_athlete(db: Session, athlete: AthleteCreate):
    if athlete.date_of_birth > datetime.date.today():
        raise HTTPException(status_code=400, detail="Invalid date of birth!")
    if len(db.query(CountriesOrm).filter(CountriesOrm.id == athlete.country_id).all()) < 1:
        raise HTTPException(status_code=400, detail="Invalid country id!")
    db_athlete = AthletesOrm(**athlete.model_dump())
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)
    return db_athlete


def update_athlete_by_id(db: Session, id: int, new_fields: AthleteCreate):
    if len(db.query(CountriesOrm).filter(CountriesOrm.id == new_fields.country_id).all()) < 1:
        raise HTTPException(status_code=404, detail="Not found this country!")

    db.query(AthletesOrm).filter(AthletesOrm.id == id).update(new_fields.model_dump())
    db.commit()


def delete_athlete_by_id(db: Session, id: int):
    if len(db.query(AthletesOrm).filter(AthletesOrm.id == id).all()) < 1:
        raise HTTPException(status_code=404, detail="The athlete with the ID data does not exist!")

    deleted = db.query(AthletesOrm).filter(AthletesOrm.id == id).first()
    db.query(AthletesOrm).filter(AthletesOrm.id == id).delete()
    db.commit()

    return deleted


def get_athlete_by_id(db: Session, id: int):
    result = db.query(AthletesOrm).filter(AthletesOrm.id == id).all()
    if len(result) < 1:
        raise HTTPException(status_code=404, detail="The athlete with this ID does not exist!")
    return AthleteModel.model_validate(result[0], from_attributes=True)
