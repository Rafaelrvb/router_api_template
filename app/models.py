from pydantic import BaseModel, field_validator, model_validator
from typing import List


class Course(BaseModel):
    id: int
    name: str
    price: float
    duree: str
    niveau: str
    langue: str

    def format_course(self):
        details = {
            "durée": self.duree,
            "niveau": self.niveau,
            "langue": self.langue,
        }
        return {
            "name": self.name,
            "id": self.id,
            "price": self.price,
            "details": details,
        }


class StudentProgress(BaseModel):
    student_id: int
    course_id: int
    progress: float


class Student(BaseModel):
    id: int
    name: str
    average_grade: float
    courses: List[StudentProgress] | None

    def format_student(self):
        formated_courses = {
            "courseId": [],
            "progression": {},
        }
        for std_prog in self.courses:
            course_id = std_prog.course_id
            progress = std_prog.progress
            formated_courses["courseId"].append(int(course_id))
            formated_courses["progression"][str(course_id)] = float(progress)

        return {
            "name": self.name,
            "student_id": self.id,
            "average_grade": self.average_grade,
            "courses": formated_courses,
        }

    # Validate student_id == StudentProgress.student_id
