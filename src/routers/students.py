from typing import Any

from fastapi import APIRouter, HTTPException

from src.models import Student, StudentBase, StudentBaseOut, StudentUpdate

router = APIRouter()

students: list[Student] = [
    Student(student_id=1, name="John Doe", age=20, email="john@example.com"),
    Student(student_id=2, name="Jane Doe", age=20, email="jane@example.com"),
    Student(student_id=3, name="Bob Ross", age=21, email="bob@example.com"),
]


@router.get("/")
async def get_students() -> list[Student]:
    return students


@router.post("/", response_model=StudentBaseOut, status_code=201)
async def create_student(new_student: StudentBase) -> Any:
    new_id = len(students) + 1
    new_student = Student(student_id=new_id, **new_student.model_dump())  # is there another way?

    students.append(new_student)
    return new_student


@router.get("/{student_id}")
async def get_student_by_id(student_id: int) -> Student:
    for s in students:
        if s.student_id == student_id:
            return s

    raise HTTPException(status_code=404, detail="Student not found")


@router.put("/{student_id}", response_model=StudentBaseOut, status_code=200)
async def update_student(student_id: int, student: StudentUpdate) -> Any:
    for s in students:
        if s.student_id == student_id:
            curr_student = Student(**s.model_dump())

            updated_student = curr_student.model_copy(update=student.model_dump(exclude_unset=True))

            students[students.index(s)] = updated_student

            return updated_student

    raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/{student_id}", status_code=200)
async def delete_student(student_id: int) -> dict[str, str]:
    for i, s in enumerate(students):
        if s.student_id == student_id:
            students.pop(i)

    return {"message": "Student deleted"}
