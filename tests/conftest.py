import pytest

from extensions import db as _db
from settings import TestingConfig
from application import create_app
from apps.user.models import User
from apps.token.models import Token


@pytest.fixture
def client():
    app = create_app(TestingConfig)

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture
def db(client):
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture
def data():
    return {
        "token": "MIIC2TCCAcMCAQAwZjFkMA4GA1UEAwwHZHNhZmRzZjATBgkqhkiG9w0BCQETBnNh",
        "user": {
            "name": "Tom",
            "email": "email@email.email",
            "password": "password123",
        },
    }


@pytest.fixture
def create_user(db, data):
    user = User(
        name=data["user"]["name"],
        email=data["user"]["email"],
        password=data["user"]["password"],
    )
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def create_token(db, create_user, data):
    token = Token(user_id=create_user.id, token=data["token"])
    db.session.add(token)
    db.session.commit()
    return token
