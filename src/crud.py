from typing import Sequence

from result import Err, Ok, Result
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import exists, select, update

from src.models import Student as StudentModel
from src.schemas import Error, ErrorStatus, StudentBase, StudentUpdate


def student_exists(db: Session, student_id: int) -> Result[bool, Error]:
    try:
        db_student = db.scalar(select(exists(StudentModel).where(StudentModel.id == student_id)))
        if not db_student:
            return Err(Error(status=ErrorStatus.NOT_FOUND, detail="Student not found"))

        return Ok(db_student)

    except SQLAlchemyError:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Database error"))

    except Exception:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"))


def get_students(db: Session, skip: int = 0, limit: int = 100) -> Result[Sequence[StudentModel], Error]:
    try:
        db_student_list = db.scalars(select(StudentModel).offset(skip).limit(limit)).all()
        return Ok(db_student_list)

    except SQLAlchemyError:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Database error"))

    except Exception:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"))


def get_student_by_id(db: Session, student_id: int) -> Result[StudentModel | None, Error]:
    try:
        db_student = db.scalar(select(StudentModel).where(StudentModel.id == student_id))
        return Ok(db_student)

    except SQLAlchemyError:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Database error"))

    except Exception:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"))


def create_student(db: Session, student_create: StudentBase) -> Result[StudentModel | None, Error]:
    try:
        db_student = StudentModel(**student_create.model_dump())
        db.add(db_student)
        db.flush()
        return Ok(db_student)

    except IntegrityError:
        return Err(Error(status=ErrorStatus.CONFLICT, detail="Student with this email already exists"))

    except SQLAlchemyError:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Database error"))

    except Exception:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"))


def update_student(db: Session, student_id: int, student_update: StudentUpdate) -> Result[StudentModel | None, Error]:
    try:
        db_student = db.execute(
            update(StudentModel)
            .where(StudentModel.id == student_id)
            .values(student_update.model_dump(exclude_unset=True))
            .returning(StudentModel)
        ).scalar_one()
        db.flush()
        return Ok(db_student)

    except IntegrityError:
        return Err(Error(status=ErrorStatus.CONFLICT, detail="Student with this email already exists"))

    except SQLAlchemyError:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Database error"))

    except Exception:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"))


def delete_student(db: Session, student_id: int) -> Result[StudentModel | None, Error]:
    try:
        db_student = db.scalar(select(StudentModel).where(StudentModel.id == student_id))
        db.delete(db_student)
        db.flush()
        return Ok(db_student)

    except SQLAlchemyError:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Database error"))

    except Exception:
        return Err(Error(status=ErrorStatus.INTERNAL_SERVER_ERROR, detail="Internal server error"))
