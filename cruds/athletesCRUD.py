import datetime
from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from orm.orm import AthletesOrm, CountriesOrm
from schemas.athletes_schemas import AthleteModel, AthleteCreate, AthletesFieldsDict
from schemas.schemas import GenderType


def create_athlete(db: Session, athlete: AthleteCreate):
    db_athlete = AthletesOrm(**athlete.model_dump())
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)


def get_athletes_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str,
        search: str | None
):
    query = select(AthletesOrm)

    if search:
        match search_field:
            case "Имя":
                if reverse == "По возрастанию":
                    query = select(AthletesOrm).filter(AthletesOrm.first_name.like(f"{search}%")).order_by(
                        AthletesFieldsDict[sort_field])
                else:
                    query = select(AthletesOrm).filter(AthletesOrm.first_name.like(f"{search}%")).order_by(
                        desc(AthletesFieldsDict[sort_field]))
            case "Фамилия":
                if reverse == "По возрастанию":
                    query = select(AthletesOrm).filter(AthletesOrm.last_name.like(f"{search}%")).order_by(
                        AthletesFieldsDict[sort_field])
                else:
                    query = select(AthletesOrm).filter(AthletesOrm.last_name.like(f"{search}%")).order_by(
                        desc(AthletesFieldsDict[sort_field]))
            case "Пол":
                gndr = GenderType.M if search == "M" else GenderType.F
                if reverse == "По возрастанию":
                    query = select(AthletesOrm).filter(AthletesOrm.gender == gndr).order_by(
                        AthletesFieldsDict[sort_field])
                else:
                    query = select(AthletesOrm).filter(AthletesOrm.gender == gndr).order_by(
                        desc(AthletesFieldsDict[sort_field]))
    else:
        if reverse == "По возрастанию":
            query = select(AthletesOrm).order_by(AthletesFieldsDict[sort_field])
        else:
            query = select(AthletesOrm).order_by(desc(AthletesFieldsDict[sort_field]))

    result = [AthleteModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result


def get_all_athletes(db: Session):
    query = select(AthletesOrm)
    res = db.execute(query)
    ans = [AthleteModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans


def get_athlete_by_id(db: Session, id: int):
    result = db.query(AthletesOrm).filter(AthletesOrm.id == id).all()

    return AthleteModel.model_validate(result[0], from_attributes=True)


def update_athlete_by_id(db: Session, id: int, new_fields: AthleteCreate):
    if len(db.query(CountriesOrm).filter(CountriesOrm.id == new_fields.country_id).all()) < 1:
        raise HTTPException(status_code=404, detail="Not found this country!")

    db.query(AthletesOrm).filter(AthletesOrm.id == id).update(new_fields.model_dump())
    db.commit()


def delete_athlete_by_id(db: Session, id: int):
    db.query(AthletesOrm).filter(AthletesOrm.id == id).delete()
    db.commit()
