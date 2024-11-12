from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from orm.medals_orm import MedalsOrm
from schemas.medals_schemas import MedalModel, MedalsFieldsDict


def get_medals_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str | None
):
    query = select(MedalsOrm)

    if search_field:
        if reverse == "По возрастанию":
            print("!!!!!!!!!!!!!!")
            query = select(MedalsOrm).filter(MedalsOrm.medal_type == search_field).order_by(
                    MedalsFieldsDict[sort_field])
        else:
            query = select(MedalsOrm).filter(MedalsOrm.medal_type == search_field).order_by(
                    desc(MedalsFieldsDict[sort_field]))
    else:
        if reverse == "По возрастанию":
            query = select(MedalsOrm).order_by(MedalsFieldsDict[sort_field])
        else:
            query = select(MedalsOrm).order_by(desc(MedalsFieldsDict[sort_field]))

    result = [MedalModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result