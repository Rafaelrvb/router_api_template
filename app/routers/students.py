from fastapi import APIRouter, Depends, HTTPException, Response
from sqlite3 import Connection
from app.dependencies import get_db
from app.database.db import list_all_students_progress, delete_student_by_id, student_progress_by_id
from app.utils import get_student_data


router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}}
)


@router.get("/list")
async def list_students(db: Connection = Depends(get_db)):
    enrollments = list_all_students_progress(db)
    list_of_students = get_student_data(enrollments)
    return [student.format_student() for student in list_of_students]


@router.get("/{student_id}")
async def read_student(student_id: int, db: Connection = Depends(get_db)):
    enrollments = student_progress_by_id(student_id, db)
    if enrollments:
        student = get_student_data(enrollments)[0]
        return student.format_student()
    else:
        raise HTTPException(status_code=404, detail="Student not found")


@router.delete("/delete/{student_id}")
async def delete_student(student_id: int, db: Connection = Depends(get_db)):
    delete_student = delete_student_by_id(student_id, db)
    if delete_student:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Student not found")
