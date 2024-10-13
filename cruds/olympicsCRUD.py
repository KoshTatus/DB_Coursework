from fastapi import Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from orm.orm import OlympicsOrm
from schemas.olympics_schemas import OlympicModel, OlympicCreate, OlympicDelete

SKIP = 0
LIMIT = 20

def get_all_olympics(db: Session, skip: int = SKIP, limit: int = LIMIT):
    return db.query(OlympicsOrm).offset(skip).limit(limit).all()

def create_olympic(db: Session, olympic: OlympicCreate):
    db_olympic = OlympicsOrm(**olympic.model_dump())
    db.add(db_olympic)
    db.commit()
    db.refresh(db_olympic)
    return db_olympic

def get_olympic_by_id(db: Session, id: int):
    result = db.query(OlympicsOrm).filter(OlympicsOrm.id == id).all()
    if len(result) < 1:
        raise HTTPException(status_code=404, detail="The athlete with this ID does not exist!")
    return OlympicModel.model_validate(result[0], from_attributes=True)

def get_all_olympics_list(db: Session, skip: int = SKIP, limit: int = LIMIT):
    query = (select(OlympicsOrm).limit(LIMIT))
    res = db.execute(query)
    ans = [OlympicModel.model_validate(row, from_attributes=True) for row in res.scalars().all()]
    return ans

def update_olympic_by_id(db: Session, new_olympic: OlympicCreate):
    if len(db.query(OlympicsOrm).filter(OlympicsOrm.id == new_olympic.id).all()) < 1:
        raise HTTPException(status_code=404, detail="The country with the ID data does not exist!")

    return db.query(OlympicsOrm).filter(OlympicsOrm.id == new_olympic.id).first()

def delete_olympic_by_id(db: Session, id: int):
    deleted = db.query(OlympicsOrm).filter(OlympicsOrm.id == id).first()
    db.query(OlympicsOrm).filter(OlympicsOrm.id == id).delete()
    db.commit()

    return deleted
