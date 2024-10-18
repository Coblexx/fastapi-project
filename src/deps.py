from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.crud import student_exists
from src.utils.get_status_code import get_status_code


def deps_student_exits(student_id: int, db: Session = Depends(get_db)) -> None:
    result = student_exists(db, student_id)

    if result.is_err():
        raise HTTPException(
            status_code=get_status_code(result.unwrap_err().status),
            detail=result.unwrap_err().detail,
        )

    return None
