import pytest
from apps.user.models import User
import email


class TestUser:
    def test_get_by_id(self, db, create_user, data):
        email = data["user"]["email"]
        retrieved = db.session.query(User).filter_by(email=email).first()

        assert retrieved == create_user

    def test_check_password(self, db, create_user, data):
        assert create_user.check_password(data["user"]["password"]) is True
        assert create_user.check_password("123") is False
        assert create_user.password != data["user"]["password"]

    def test_fields(self, db, data):
        user = User(**data["user"])
        db.session.add(user)
        db.session.commit()

        assert user.name == data["user"]["name"]
        assert user.email == data["user"]["email"]
