from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, schemas
from src.core.db import get_db

router = APIRouter()


@router.get("/", response_model=Sequence[schemas.Student])
async def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> Sequence[schemas.Student]:
    students = crud.get_students(db, skip=skip, limit=limit)
    return students


@router.post("/", response_model=schemas.StudentBaseOut, status_code=201)
async def create_student(new_student: schemas.StudentBase, db: Session = Depends(get_db)) -> schemas.StudentBaseOut:
    student = crud.create_student(db, schemas.StudentBase(**new_student.model_dump()))
    return student


@router.get("/{student_id}", response_model=schemas.Student)
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)) -> schemas.Student:
    student = crud.get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@router.put("/{student_id}", response_model=schemas.StudentBaseOut, status_code=200)
async def update_student(
    student_id: int, update_student_data: schemas.StudentUpdate, db: Session = Depends(get_db)
) -> schemas.Student | None:

    updated_student = crud.update_student(db, student_id, update_student_data)

    if updated_student:
        return updated_student

    raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/{student_id}", status_code=204)
async def delete_student(student_id: int, db: Session = Depends(get_db)) -> None:
    crud.delete_student(db, student_id)
