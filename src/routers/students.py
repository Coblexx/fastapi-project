from typing import Sequence, Tuple

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.crud import create_student, delete_student, get_student_by_id, get_students, update_student
from src.models import Student as StudentModel
from src.schemas import Student as StudentSchema
from src.schemas import StudentBase, StudentBaseOut, StudentUpdate

router = APIRouter()


async def common_params(student_id: int, db: Session = Depends(get_db)) -> tuple[Session, int]:
    return db, student_id


CommonDeps = Tuple[Session, int]


@router.get("/", response_model=Sequence[StudentSchema])
async def get_students_list(db: Session = Depends(get_db), limit: int = 100, skip: int = 0) -> Sequence[StudentModel]:
    try:
        students = get_students(db, skip=skip, limit=limit)
        if not students:
            raise HTTPException(status_code=404, detail="No students found")

        return students

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"An error occurred while fetching students: {e}")


@router.post("/", response_model=StudentBaseOut, status_code=201)
async def create_new_student(new_student: StudentBase, db: Session = Depends(get_db)) -> StudentModel | None:
    try:
        student = create_student(db, StudentBase(**new_student.model_dump()))
        if not student:
            raise HTTPException(status_code=400, detail="Student could not have been created!")
        return student

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while creating student: {e}")


@router.get("/{student_id}", response_model=StudentSchema)
async def get_existing_student_by_id(commons: CommonDeps = Depends(common_params)) -> StudentModel | None:
    try:
        db, student_id = commons
        student = get_student_by_id(db, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return student

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"An error occured while fetching student data: {e}")


@router.put("/{student_id}", response_model=StudentBaseOut, status_code=200)
async def update_existing_student(
    update_student_data: StudentUpdate, commons: CommonDeps = Depends(common_params)
) -> StudentModel | None:
    try:
        db, student_id = commons
        updated_student = update_student(db, student_id, update_student_data)

        if not updated_student:
            raise HTTPException(status_code=404, detail="Student could not have been updated!")

        return updated_student

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"An error occured while updating student: {e}")


@router.delete("/{student_id}", status_code=204)
async def delete_student_by_id(commons: CommonDeps = Depends(common_params)) -> None:
    try:
        db, student_id = commons
        delete_student(db, student_id)

    except Exception:
        raise HTTPException(status_code=404, detail="An error occured while deleting student!")
