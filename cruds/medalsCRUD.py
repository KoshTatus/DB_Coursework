from fastapi import Query, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from orm.orm import MedalsOrm
from schemas.schemas import MedalCreate, MedalModel

SKIP = 0
LIMIT = 20

def get_sorted_medals_list(db: Session, reverse: bool = False, skip: int = SKIP, limit: int = LIMIT):
    if reverse:
        query = select(MedalsOrm).order_by(desc("medal_type"))
    else:
        query = select(MedalsOrm).order_by("medal_type")

    result = [MedalModel.model_validate(row, from_attributes=True) for row in db.execute(query).scalars().all()]

    return result

def get_all_medals(db: Session, skip: int = SKIP, limit: int = LIMIT):
    return db.query(MedalsOrm).offset(skip).limit(limit).all()

def create_medal(db: Session, event: MedalCreate):
    db_medal = MedalsOrm(**event.model_dump())
    db.add(db_medal)
    db.commit()
    db.refresh(db_medal)
    return db_medal

def get_medal_by_id(db: Session, id: int):
    print("!!!!!!!!!!!!!!!")
    result = db.query(MedalsOrm).filter(MedalsOrm.id == id).all()
    return MedalModel.model_validate(result[0], from_attributes=True)

def get_all_medals_list(db: Session, skip: int = SKIP, limit: int = LIMIT):
    query = (select(MedalsOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [MedalModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans

def update_medal_by_id(db: Session, new_medal: MedalCreate):
    if len(db.query(MedalsOrm).filter(MedalsOrm.id == new_medal.id).all()) < 1:
        raise HTTPException(status_code=404, detail="The country with the ID data does not exist!")

    return db.query(MedalsOrm).filter(MedalsOrm.id == new_medal.id).first()

def delete_medal_by_id(db: Session, id: int):
    deleted = db.query(MedalsOrm).filter(MedalsOrm.id == id).first()
    db.query(MedalsOrm).filter(MedalsOrm.id == id).delete()
    db.commit()

    return deleted
