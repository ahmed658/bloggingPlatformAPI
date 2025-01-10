from fastapi.testclient import TestClient
from app.main import blogApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.config import settings
from app.services.oauth2_service import create_jwt_token
from app import schemas
import pytest

SQLALCHEMY_TESTING_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_TESTING_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope = "function")
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope = "function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    blogApp.dependency_overrides[get_db] = override_get_db
    yield TestClient(blogApp)
    
@pytest.fixture
def test_user(client):
    user_data = {
    "username": "maher",
    "password": "password-for-test-user",
    "first_name": "ahmed",
    "last_name": "maher",
    "email": "ahmedmaherbf@gmail.com"
    }
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client, test_user):
    user_data = {
    "username": "maher2",
    "password": "password-for-test-user2",
    "first_name": "ahmed",
    "last_name": "maher",
    "email": "ahmedmaherbf2@gmail.com"
    }
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    access_token = create_jwt_token(data={"user_id": test_user['user_id']})
    token = schemas.Token(access_token= access_token, token_type= "bearer")
    return token

@pytest.fixture(scope = "function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"{token.token_type} {token.access_token}"
    }
    
    return client

@pytest.fixture
def token2(test_user2):
    access_token = create_jwt_token(data={"user_id": test_user2['user_id']})
    token = schemas.Token(access_token= access_token, token_type= "bearer")
    return token

@pytest.fixture(scope = "function")
def authorized_client2(client, token2):
    client.headers = {
        **client.headers,
        "Authorization": f"{token2.token_type} {token2.access_token}"
    }
    
    return client

# Fixture to create an admin user
@pytest.fixture
def admin_user(client, session):
    user_data = {
        "username": "adminuser",
        "password": "adminpassword",
        "first_name": "Admin",
        "last_name": "User",
        "email": "adminuser@example.com",
        "admin": True,
        "root_pass": settings.root_pass
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# Fixture to create an authorized admin client
@pytest.fixture
def admin_client(client, admin_user):
    access_token = create_jwt_token(data={"user_id": admin_user['user_id']})
    client.headers = {
        **client.headers,
        "Authorization": f"bearer {access_token}"
    }
    return client
@pytest.fixture()
def test_posts(authorized_client):
    posts_data = [{
    "title" : "Post 1 Title",
    "content" : "Post 1 Content"
    }, {
    "title" : "Post 2 Title",
    "content" : "Post 2 Content"
    }, {
    "title" : "Post 3 Title",
    "content" : "Post 3 Content"
    }]
    
    posts_responses = []
    
    for post in posts_data:
        res = authorized_client.post("/posts/", json=post)
        assert res.status_code == 201
        posts_responses.append(res.json())
        
    return posts_responses
        
        