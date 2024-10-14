from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select, update

from src import models, schemas


def get_students(db: Session, skip: int = 0, limit: int = 100) -> Sequence[models.Student]:
    try:
        return db.scalars(select(models.Student).offset(skip).limit(limit)).all()

    except Exception as e:
        print(f"An error occurred while fetching students: {e}")
        return None


def get_student_by_id(db: Session, student_id: int) -> models.Student | None:
    try:
        return db.scalar(select(models.Student).where(models.Student.id == student_id))

    except Exception as e:
        print(f"An error occurred while fetching student: {e}")
        return None


def create_student(db: Session, student_create: schemas.StudentBase) -> models.Student | None:
    try:
        db_student = models.Student(**student_create.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    except Exception as e:
        print(f"An error occurred while creating student: {e}")
        db.rollback()
        return None


def update_student(db: Session, student_id: int, student_update: schemas.StudentUpdate) -> models.Student | None:
    try:
        db_student = db.scalar(select(models.Student).where(models.Student.id == student_id))

        db.execute(
            update(models.Student)
            .where(models.Student.id == student_id)
            .values(student_update.model_dump(exclude_unset=True))
        )

        db.commit()
        db.refresh(db_student)
        return db_student

    except Exception as e:
        print(f"An error occurred while updating student: {e}")
        db.rollback()
        return None


def delete_student(db: Session, student_id: int) -> models.Student | None:
    try:
        db_student = db.scalar(select(models.Student).where(models.Student.id == student_id))
        if db_student is None:
            print(f"Student with id {student_id} not found.")
            return None
        db.delete(db_student)
        db.commit()
        return db_student

    except Exception as e:
        print(f"An error occurred while deleting student: {e}")
        db.rollback()
        return None
