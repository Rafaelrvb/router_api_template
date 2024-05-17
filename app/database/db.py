import sqlite3
from fastapi import HTTPException


def connect_db(database: str = 'database.db'):

    conn = sqlite3.connect(database)

    # Ensures ON DELETE CASCADE for table integrity
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Create table courses
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price FLOAT,
            duree TEXT,
            niveau TEXT,
            langue TEXT
        )
    """
    )

    # Create table students
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            avg_grade FLOAT
        )
    """
    )

    # Create table enrollments
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            student_id INTEGER,
            progression FLOAT,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    """
    )

    conn.commit()
    return conn

#! Students queries
def list_all_students_progress(db: sqlite3.Connection):
    """
    Returned data: [(student_id, name, avg_grade, course_id, progression), (...)]
    """
    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT students.id, students.name, students.avg_grade, enrollments.course_id, enrollments.progression
            FROM students
            JOIN enrollments ON students.id = enrollments.student_id
            """
        )
        st_progress = cursor.fetchall()

        return st_progress
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e)


def student_progress_by_id(student_id: int, db: sqlite3.Connection):
    """
    Returned data: [(student_id, name, avg_grade, course_id, progression), (...)]
    """
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT students.id, students.name, students.avg_grade, enrollments.course_id, enrollments.progression
            FROM students
            JOIN enrollments ON students.id = enrollments.student_id
            WHERE students.id = ?
            """, (student_id,)
        )
        st_progress = cursor.fetchall()

        return st_progress
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e)


def delete_student_by_id(student_id: int, db: sqlite3.Connection):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        db.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e)


#! Courses queries
def list_all_courses(db: sqlite3.Connection):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        return courses
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e)


def get_course_by_id(course_id: int, db: sqlite3.Connection):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM courses WHERE id = ?",(course_id,))
        course = cursor.fetchone()

        return course
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e)


def delete_course_by_id(course_id: int, db: sqlite3.Connection):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        db.commit()
        return cursor.rowcount
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=e)
