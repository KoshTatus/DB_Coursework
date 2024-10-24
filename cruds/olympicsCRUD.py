from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.olympics_orm import OlympicsOrm
from schemas.olympics_schemas import OlympicsFieldsDict, OlympicModel


def get_olympics_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str | None,
        search: str | None
):
    query = select(OlympicsOrm)

    if search:
        match search_field:
            case "Место проведения":
                if reverse == "По возрастанию":
                    query = select(OlympicsOrm).filter(OlympicsOrm.location.like(f"{search}%")).order_by(
                            OlympicsFieldsDict[sort_field])
                else:
                    query = select(OlympicsOrm).filter(OlympicsOrm.location.like(f"{search}%")).order_by(
                        desc(OlympicsFieldsDict[sort_field]))
            case "Сезон":
                season = 'd'
                if reverse == "По возрастанию":
                    query = select(OlympicsOrm).filter(OlympicsOrm.season.like(f"{search}%")).order_by(
                        OlympicsFieldsDict[sort_field])
                else:
                    query = select(OlympicsOrm).filter(OlympicsOrm.season.like(f"{search}%")).order_by(
                        desc(OlympicsFieldsDict[sort_field]))
    else:
        if reverse == "По возрастанию":
            query = select(OlympicsOrm).order_by(OlympicsFieldsDict[sort_field])
        else:
            query = select(OlympicsOrm).order_by(desc(OlympicsFieldsDict[sort_field]))

    result = [OlympicModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result