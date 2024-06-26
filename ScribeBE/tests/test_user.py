from httpx import ASGITransport, AsyncClient
import pytest
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

from main import app
from database.database import Database
from models.user_model import DbUser
from database.connection import Settings
import auth.JWT_token as JWT_token
from datetime import timedelta
from auth.JWT_token import create_access_token


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


async def init_db():
    settings = Settings()
    await settings.initialize_database()


@pytest.fixture
async def access_token() -> str:
    return create_access_token(data={
                "sub": str(ObjectId('661efe6b374bc649942efd81')),
                "email_id": 'a@gmail.com',
                "password": "a123"
            },
            expires_delta=timedelta(
                minutes=JWT_token.ACCESS_TOKEN_EXPIRE_MINUTES 
            ))

################# signup TESTCASE ########################################

@pytest.mark.asyncio
async def test_signup() -> None:
    
    await init_db()
    # Clean test data
    user_database = Database(DbUser)
    await user_database.delete_all_by_field("email", "pytest@gmail.com")

    payload = {"name" : "pytest", "email": "pytest@gmail.com", "password": "pytest123"}
    headers = {"Content-Type": "application/json"}
    test_response = "successfully add new user"
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        response = await client.post("/users/signup", json=payload, headers=headers)

    json_response = response.json()
    msg = json_response["msg"]

    assert response.status_code == 201
    assert msg == test_response

@pytest.mark.asyncio
async def test_signup_with_exist_user() -> None:

    await init_db()

    payload = {"name" : "a", "email": "a@gmail.com", "password": "a123"}
    headers = {"Content-Type": "application/json"}
    test_response = {"detail" : "A user with this email already exists."}
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        response = await client.post("/users/signup", json=payload, headers=headers)
    
    assert response.status_code == 409
    assert response.json() == test_response

################# LOGIN TESTCASE########################################

@pytest.mark.asyncio
async def test_login(access_token: str) -> None:

    await init_db()

    token = await access_token
    payload = {"email": "a@gmail.com", "password": "a123"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        response = await client.post("/users/login", json=payload, headers=headers)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_with_user_not_existing(access_token: str) -> None:

    await init_db()

    token = await access_token
    payload = {"email": "", "password": ""}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    test_response = {"detail" : "Incorrect email or password, or user does not exist."}
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost:8000"
    ) as client:
        response = await client.post("/users/login", json=payload, headers=headers)

    assert response.status_code == 400
    assert response.json() == test_response