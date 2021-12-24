import pytest
from fastapi import status
from jose import jwt
from app import schemas
from app.config import settings




def test_create_user(client):
    res = client.post("/users/", json={"email": "paula@email.com", "password": "paula"})
    
    # **res.json() desempacota a resposta 
    new_user = schemas.UserResponse(**res.json())
    #assert res.json().get("email") == "paula@email.com"
    assert res.status_code ==  status.HTTP_201_CREATED
    assert new_user.email == "paula@email.com"


def test_login_user(test_user, client):
    res = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    
    login_res = schemas.Token(**res.json()) 
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")

    assert id == test_user['id'] 
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("email, password, status_code", [
    ('admin@email.com', 'password123', 403),  # email correto / senha incorreta
    ('dummyemail@gmail.com', 'admin', 403),   # email incorreto / senha incorreta
    ('dummyemail@gmail.com', 'password123', 403),
    (None, 'password123', 422),
    ('dummyEmail@gmail.com', None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login/", data={"username": email, "password": password})

    assert res.status_code == status_code

    # assert res.json().get('detail') == 'Invalid Credentials' 