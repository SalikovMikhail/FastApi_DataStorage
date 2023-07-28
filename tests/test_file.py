import pytest
from sqlalchemy import insert, select


from conftest import client, async_session_maker


HEADERS =  {'Content-Type': 'application/x-www-form-urlencoded'}

def login() -> str:
    response = client.post(
        "/auth/jwt/login",
        data={
            "username": "test@yandex.ru",
            "password": "pas123",
            "grant_type": "password"
        },
        headers=HEADERS
    )

    api_key = response.cookies.get('bonds')
    return api_key


def test_add_file():

    api_key = login()

    response = client.post(
        "/file/",
        files={'file': open('books.csv', 'rb')},
        cookies={'bonds': api_key}
    )

    assert response.status_code == 200


def test_get_file():
    api_key = login()

    response = client.get(
        "/file/1",
        cookies={'bonds': api_key}
    )

    assert response.status_code == 200


def test_get_keys_file():

    api_key = login()

    response = client.get(
        "/file/keys/1",
        cookies={'bonds': api_key}
    )

    data = response.json()

    group_keys = ['Author', 'Name', 'Count_page', 'Genre']

    for key in group_keys:
        assert key in data

    assert response.status_code == 200


def test_gel_all_files_user():

    data = [
        {
            "id": 1,
            "name": "books.csv",
            "download_at": "2023-07-28T12:50:46.371452",
            "user": 1,
            "path": "/home/mikhail/Desktop/projects/backend/app/src/files/books.csv"
        },
        {
            "id": 2,
            "name": "books (copy).csv",
            "download_at": "2023-07-27T10:43:20.644428",
            "user": 1,
            "path": "/home/mikhail/Desktop/projects/backend/app/src/files/books (copy).csv"
        }
    ]

    api_key = login()

    response = client.post(
        "/file/",
        files={'file': open('books (copy).csv', 'rb')},
        cookies={'bonds': api_key}
    )

    response = client.get(
        "/file/",
        cookies={'bonds': api_key}
    )

    data_resp = response.json()
    #print(data_resp)

    count = 0

    for book in data_resp:

        b = data[count]

        assert book['id'] == b['id']
        assert book['name'] == b['name']
        assert book['user'] == b['user']
        assert book['path'] == b['path']

        count += 1


    #assert data == data_resp

    assert response.status_code == 200

def test_delete_file():

    api_key = login()

    response = client.delete(
        "/file/1",
        cookies={'bonds': api_key}
    )

    assert response.status_code == 200
