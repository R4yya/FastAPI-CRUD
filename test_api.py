
from fastapi.testclient import TestClient
from fastapi import FastAPI
from routers import user as UserRouter
import pytest
from models.user import User
from database import Base, engine, SessionLocal


@pytest.fixture(scope='module')
def test_client():
    app = FastAPI()
    app.include_router(UserRouter.router, prefix='/user')

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='module')
def test_db():
    db = SessionLocal()

    Base.metadata.create_all(bind=engine)

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_tables(test_db):
    test_db.query(User).delete()
    test_db.commit()


def test_create_user(test_client, test_db):
    user_data = {'name': 'test_user'}

    response = test_client.post('/user/', json=user_data)

    assert response.status_code == 200
    assert response.json()['name'] == user_data['name']


def test_get_user(test_client, test_db):
    user = User(name='test_user')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    response = test_client.get(f'/user/{user.id}')
    assert response.status_code == 200
    assert response.json()['name'] == user.name


def test_update_user(test_client, test_db):
    user = User(name='test_user')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    updated_user_data = {'name': 'updated_test_user'}
    response = test_client.put(f'/user/{user.id}', json=updated_user_data)
    assert response.status_code == 200
    assert response.json()['name'] == updated_user_data['name']


def test_delete_user(test_client, test_db):
    user = User(name='test_user')
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    response = test_client.delete(f'/user/{user.id}')
    assert response.status_code == 200
    assert response.json() == 1
