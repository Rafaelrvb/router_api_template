from app.database.db import connect_db
import os

def generate_seed(database = "database.db"):
    conn = connect_db(database)
    cursor = conn.cursor()

    # Seed Students:
    cursor.execute(
        "INSERT INTO students (id, name, avg_grade) VALUES (?, ?, ?)",
        (201, "Alice Dupont", 15.5),
    )
    cursor.execute(
        "INSERT INTO students (id, name, avg_grade) VALUES (?, ?, ?)",
        (202, "Bob Martin", 17.2),
    )
    cursor.execute(
        "INSERT INTO students (id, name, avg_grade) VALUES (?, ?, ?)",
        (203, "Clara Legrand", 14.0),
    )

    # Seed Courses:
    cursor.execute(
        "INSERT INTO courses (id, name, price, duree, niveau, langue) VALUES (?, ?, ?, ?, ?, ?)",
        (
            101,
            "Introduction à la Programmation Python",
            49.99,
            "4 semaines",
            "Débutant",
            "Français",
        ),
    )
    cursor.execute(
        "INSERT INTO courses (id, name, price, duree, niveau, langue) VALUES (?, ?, ?, ?, ?, ?)",
        (
            102,
            "Data Science Avancé",
            199.99,
            "8 semaines",
            "Avancé",
            "Anglais",
        ),
    )
    cursor.execute(
        "INSERT INTO courses (id, name, price, duree, niveau, langue) VALUES (?, ?, ?, ?, ?, ?)",
        (
            103,
            "Développement Web Full Stack",
            299.99,
            "12 semaines",
            "Intermédiaire",
            "Français",
        ),
    )

    # Seed Enrollments
    cursor.execute(
        "INSERT INTO enrollments (course_id, student_id, progression) VALUES (?, ?, ?)",
        (101, 201, 1),
    )
    cursor.execute(
        "INSERT INTO enrollments (course_id, student_id, progression) VALUES (?, ?, ?)",
        (102, 201, 0.75),
    )

    cursor.execute(
        "INSERT INTO enrollments (course_id, student_id, progression) VALUES (?, ?, ?)",
        (103, 202, 0.5),
    )

    cursor.execute(
        "INSERT INTO enrollments (course_id, student_id, progression) VALUES (?, ?, ?)",
        (101, 203, 1),
    )
    #! progression data wrong?
    cursor.execute(
        "INSERT INTO enrollments (course_id, student_id, progression) VALUES (?, ?, ?)",
        (103, 203, 25),
    )
    cursor.close()
    conn.commit()

    return conn


if __name__ == "__main__":
    try:
        if os.path.exists("database.db"):
            os.remove("database.db")
            print("Database deleted")
            conn = generate_seed()
            conn.close()
            print("Seed generated")
    except Exception as e:
        raise(e)
