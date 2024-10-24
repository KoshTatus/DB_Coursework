from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.sports_orm import SportsOrm
from schemas.sports_schemas import SportModel, SportsFieldsDict


def get_sports_list(
        db: Session,
        sort_field: str,
        reverse: str,
        search_field: str,
        search: str | None
):
    query = select(SportsOrm)

    if search:
        match search_field:
            case "Название":
                if reverse == "По возрастанию":
                    query = select(SportsOrm).filter(SportsOrm.sport_name.like(f"{search}%")).order_by(
                        SportsFieldsDict[sort_field])
                else:
                    query = select(SportsOrm).filter(SportsOrm.sport_name.like(f"{search}%")).order_by(
                        desc(SportsFieldsDict[sort_field]))
            case "Категория":
                if reverse == "По возрастанию":
                    query = select(SportsOrm).filter(SportsOrm.category.like(f"{search}%")).order_by(
                        SportsFieldsDict[sort_field])
                else:
                    query = select(SportsOrm).filter(SportsOrm.category.like(f"{search}%")).order_by(
                        desc(SportsFieldsDict[sort_field]))
    else:
        if reverse == "По возрастанию":
            query = select(SportsOrm).order_by(SportsFieldsDict[sort_field])
        else:
            query = select(SportsOrm).order_by(desc(SportsFieldsDict[sort_field]))

    result = [SportModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result
