from typing import Sequence, Tuple

from fastapi import APIRouter, Depends, HTTPException
from result import Err, Ok
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.crud import create_student, delete_student, get_student_by_id, get_students, update_student
from src.deps import deps_student_exits
from src.models import Student as StudentModel
from src.schemas import Student as StudentSchema
from src.schemas import StudentBase, StudentBaseOut, StudentUpdate
from src.utils.get_status_code import get_status_code

router = APIRouter()


async def common_params(student_id: int, db: Session = Depends(get_db)) -> tuple[Session, int]:
    return db, student_id


CommonDeps = Tuple[Session, int]


@router.get(
    "/",
    response_model=Sequence[StudentSchema],
    status_code=200,
    responses={
        200: {"description": "List of students"},
        404: {"description": "No students found"},
        500: {"description": "Internal server error"},
    },
)
async def get_student_list(db: Session = Depends(get_db), limit: int = 100, skip: int = 0) -> Sequence[StudentModel]:
    match get_students(db, skip=skip, limit=limit):
        case Ok(result):
            return result
        case Err(result):
            raise HTTPException(status_code=get_status_code(result.status), detail=result.detail)


@router.post(
    "/",
    response_model=StudentBaseOut,
    status_code=201,
    responses={
        201: {"description": "Student created"},
        409: {"description": "Student with this email already exists"},
        500: {"description": "Internal server error"},
    },
)
async def create_new_student(new_student: StudentBase, db: Session = Depends(get_db)) -> StudentModel | None:
    match create_student(db, StudentBase(**new_student.model_dump())):
        case Ok(result):
            return result
        case Err(result):
            raise HTTPException(status_code=get_status_code(result.status), detail=result.detail)


@router.get(
    "/{student_id}",
    response_model=StudentSchema,
    status_code=200,
    dependencies=[Depends(deps_student_exits)],
    responses={
        200: {"description": "Student found"},
        404: {"description": "Student not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_existing_student_by_id(commons: CommonDeps = Depends(common_params)) -> StudentModel | None:
    db, student_id = commons

    match get_student_by_id(db, student_id):
        case Ok(result):
            return result
        case Err(result):
            raise HTTPException(status_code=get_status_code(result.status), detail=result.detail)


@router.put(
    "/{student_id}",
    response_model=StudentBaseOut,
    status_code=200,
    responses={
        200: {"description": "Student updated"},
        404: {"description": "Student not found"},
        409: {"description": "Student with this email already exists"},
        500: {"description": "Internal server error"},
    },
    dependencies=[Depends(deps_student_exits)],
)
async def update_existing_student(
    update_student_data: StudentUpdate, commons: CommonDeps = Depends(common_params)
) -> StudentModel | None:
    db, student_id = commons

    match update_student(db, student_id, update_student_data):
        case Ok(result):
            return result
        case Err(result):
            raise HTTPException(status_code=get_status_code(result.status), detail=result.detail)


@router.delete(
    "/{student_id}",
    status_code=204,
    responses={
        204: {"description": "Student deleted"},
        500: {"description": "Internal server error"},
    },
)
async def delete_student_by_id(commons: CommonDeps = Depends(common_params)) -> None:
    try:
        db, student_id = commons
        delete_student(db, student_id)

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
