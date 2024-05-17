from fastapi import APIRouter, HTTPException, Depends, Response
from sqlite3 import Connection
from app.dependencies import get_db
from app.database.db import list_all_courses, get_course_by_id, delete_course_by_id
from app.models import Course
from typing import List


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list_courses(db: Connection = Depends(get_db)):
    courses_db = list_all_courses(db)
    courses: List[Course] = []

    for course in courses_db:
        id, name, price, duree, niveau, langue = course
        try:
            course_obj = Course(
                id=id,
                name=name,
                price=price,
                duree=duree,
                niveau=niveau,
                langue=langue
            ).format_course()
            courses.append(course_obj)
        except Exception:
            raise HTTPException(status_code=500, detail=f"Could not create course object")

    return courses


@router.get("/{course_id}")
async def read_course(course_id: int, db: Connection = Depends(get_db)):
    course = get_course_by_id(course_id, db)
    if course:
        id, name, price, duree, niveau, langue = course
        try:
            course_obj = Course(
                id=id,
                name=name,
                price=price,
                duree=duree,
                niveau=niveau,
                langue=langue
            ).format_course()
            return course_obj
        except Exception:
            raise HTTPException(status_code=500, detail=f"Could not create course object")
    else:
        raise HTTPException(status_code=404, detail="course not found")


@router.delete("/delete/{course_id}")
async def delete_course(course_id: int, db: Connection = Depends(get_db)):
    delete_course = delete_course_by_id(course_id, db)
    if delete_course:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Course not found")
