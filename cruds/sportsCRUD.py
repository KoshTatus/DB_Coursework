from fastapi import Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from orm.orm import SportsOrm
from schemas.sports_schemas import SportModel, SportCreate, SportDelete

SKIP = 0
LIMIT = 20

def get_all_sports(db: Session, skip: int = SKIP, limit: int = LIMIT):
    return db.query(SportsOrm).offset(skip).limit(limit).all()

def get_sport_by_name(db: Session, sport_name):
    return db.query(SportsOrm).filter(SportsOrm.sport_name == sport_name).first()

def create_sport(db: Session, event: SportCreate):
    db_sport = SportsOrm(**event.model_dump())
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport

def get_sport_by_id(db: Session, id: int):
    result = db.query(SportsOrm).filter(SportsOrm.id == id).all()
    if len(result) < 1:
        raise HTTPException(status_code=404, detail="The athlete with this ID does not exist!")
    return SportModel.model_validate(result[0], from_attributes=True)

def get_all_sports_list(db: Session, skip: int = SKIP, limit: int = LIMIT):
    query = (select(SportsOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [SportModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans

def update_sport_by_id(db: Session, new_sport: SportCreate):
    if len(db.query(SportsOrm).filter(SportsOrm.id == new_sport.id).all()) < 1:
        raise HTTPException(status_code=404, detail="The country with the ID data does not exist!")

    return db.query(SportsOrm).filter(SportsOrm.id == new_sport.id).first()

def delete_sport_by_id(db: Session, id: int):
    deleted = db.query(SportsOrm).filter(SportsOrm.id == id).first()
    db.query(SportsOrm).filter(SportsOrm.id == id).delete()
    db.commit()

    return deleted
