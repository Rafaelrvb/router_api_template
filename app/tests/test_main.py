import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db import delete_student_by_id, delete_course_by_id
from seed import generate_seed
client = TestClient(app)

#! Testing API connection and Routes
def test_get_home():
    response = client.get("/", headers={"token": "my_token"})
    assert response.status_code == 200


def test_get_student_list_route():
    response = client.get("/students/list", headers={"token": "my_token"})
    assert response.status_code == 200


def test_get_courses_list_route():
    response = client.get("/courses/list", headers={"token": "my_token"})
    assert response.status_code == 200


def test_get_course_by_id():
    response = client.get("/courses/101", headers={"token": "my_token"})
    assert response.status_code == 200


def test_get_course_by_id_invalid():
    response = client.get("/courses/10", headers={"token": "my_token"})
    assert response.status_code == 404


def test_get_course_by_id_invalid():
    response = client.get("/courses/10", headers={"token": "my_token"})
    assert response.status_code == 404


def test_delete_course_by_id_invalid():
    response = client.delete("/courses/delete/10", headers={"token": "my_token"})
    assert response.status_code == 404


#! Testing DB functions
@pytest.fixture
def sqlsession():
    conn = generate_seed(":memory:")
    yield conn
    conn.close()

def test_delete_student_by_id(sqlsession):
    assert delete_student_by_id(201, sqlsession) == 1


def test_delete_course_by_id(sqlsession):
    assert delete_course_by_id(101, sqlsession) == 1
