from typing import Type
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.database import Base


def create_object(
        db: Session,
        create_obj: Type[BaseModel],
        table: Type[Base]
):
    db_object = table(**create_obj.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)


def get_all_objects(
        db: Session,
        model: Type[BaseModel],
        table: Type[Base]
):
    return [model.model_validate(row, from_attributes=True) for row in db.execute(select(table)).scalars().all()]


def get_object_by_id(
        db: Session,
        id: int,
        model: Type[BaseModel],
        table: Type[Base]
):
    result = db.query(table).filter(table.id == id).all()

    return model.model_validate(result[0], from_attributes=True)


def update_object_by_id(
        db: Session,
        id: int,
        new_object: Type[BaseModel],
        table: Type[Base]
):
    db.query(table).filter(table.id == id).update(new_object.model_dump())
    db.commit()


def delete_object_by_id(
        db: Session,
        id: int,
        table: Type[Base]
):
    db.query(table).filter(table.id == id).delete()
    db.commit()
