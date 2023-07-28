import pytest
from sqlalchemy import insert, select


from conftest import client, async_session_maker

HEADERS =  {'Content-Type': 'application/x-www-form-urlencoded'}

def test_register():
    response = client.post("/auth/register", json={
        "email": "test@yandex.ru",
        "password": "pas123",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "test123",
    })

    assert response.status_code == 201

def test_auth():
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "test@yandex.ru",
            "password": "pas123",
            "grant_type": "password"
        },
        headers=HEADERS
    )

    assert response.status_code == 204
