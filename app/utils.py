from fastapi import HTTPException
from app.models import Student, StudentProgress
from typing import List

def get_student_data(enrollments) -> List[Student]:
    '''
    Helper function to get Student data and Enrollments data to create a Student object
    with proper StudentProgress data.
    '''
    students = {}
    try:
        for std_progress in enrollments:
            student_id, name, avg_grade, course_id, progression = std_progress

            # If student already created -> append new student progression to the existing Student object
            if student_id in students:
                new_std_progress = StudentProgress(
                    student_id=student_id, course_id=course_id, progress=progression
                )
                students[student_id].courses.append(new_std_progress)

            # Creates a new Student object and tracks it in the students dict
            else:
                new_student = Student(
                    id=student_id,
                    name=name,
                    average_grade=avg_grade,
                    courses=[
                        StudentProgress(
                            student_id=student_id,
                            course_id=course_id,
                            progress=progression,
                        )
                    ],
                )
                students[student_id] = new_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    return list(students.values())
