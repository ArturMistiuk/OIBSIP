import pytest

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


@pytest.mark.parametrize(('username', 'password', 'confirm_password', 'status_code'), [
    ('testusername', 'testpassword', 'testpassword', 201),
    ('testusername', 'password', 'testpassword', 422),
    ('testusername', 'pass', 'pass', 422),
    ('test_username', 'pass_word', 'pass_word', 422),
])
def test_register_user_success(username, password, confirm_password, status_code):
    response = client.post("/auth/register", json={'username': username, 'password': password, 'confirm_password': confirm_password})
    assert response.status_code == status_code


@pytest.mark.parametrize(('username', 'password', 'status_code'), [
    ('testusername', 'testpassword', 401),
])
def test_login_user_incorrect_credentials(username, password, status_code):
    incorrect_credentials = {'username': 'wrong_user', 'password': 'wrong_password'}
    response = client.post("/auth/login", json=incorrect_credentials)
    assert response.status_code == 401


def test_secured_page_access_without_token():
    response = client.post("/auth/secured_page")
    assert response.status_code == 401


def test_secured_page_access_with_invalid_token():
    response = client.post("/auth/secured_page")
    assert response.status_code == 401
