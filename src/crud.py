from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from src import models, schemas


def get_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[models.Student]:
    return db.scalars(select(models.Student).offset(skip).limit(limit)).all()


def get_student_by_id(db: Session, student_id: int) -> models.Student | None:
    return db.scalar(select(models.Student).where(models.Student.id == student_id))


def create_student(db: Session, student_create: schemas.StudentBase) -> models.Student:
    db_student = models.Student(**student_create.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate) -> schemas.Student | None:
    db_student = db.scalar(select(models.Student).where(models.Student.id == student_id))

    for key, value in student_update.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int) -> models.Student | None:
    db_student = db.scalar(select(models.Student).where(models.Student.id == student_id))
    db.delete(db_student)
    db.commit()
    return db_student
