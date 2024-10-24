from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from orm.athletes_orm import AthletesOrm
from schemas.athletes_schemas import AthleteModel, AthletesFieldsDict, AthleteCreateToCountry
from schemas.schemas import GenderType


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
                gndr = "No"
                if search == "M":
                    gndr = GenderType.M
                elif search == "F":
                    gndr = GenderType.F
                if gndr != "No":
                    if reverse == "По возрастанию":
                        query = select(AthletesOrm).filter(AthletesOrm.gender == gndr).order_by(
                            AthletesFieldsDict[sort_field])
                    else:
                        query = select(AthletesOrm).filter(AthletesOrm.gender == gndr).order_by(
                            desc(AthletesFieldsDict[sort_field]))
                else:
                    return []
    else:
        if reverse == "По возрастанию":
            query = select(AthletesOrm).order_by(AthletesFieldsDict[sort_field])
        else:
            query = select(AthletesOrm).order_by(desc(AthletesFieldsDict[sort_field]))

    result = [AthleteModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result

def create_athlete_to_country(id: int, form: AthleteCreateToCountry, db: Session):
    fields = form.model_dump()
    fields.update(dict(country_id=str(id)))
    db_athlete = AthletesOrm(**fields)
    db.add(db_athlete)
    db.commit()
    db.refresh(db_athlete)