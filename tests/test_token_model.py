import pytest
from apps.token.models import Token
from apps.user.models import User


# @pytest.fixture
# def user_id(db):
#     user = User(name="test", email="XXXXXXXXXXXXXX", password="test")
#     db.session.add(user)
#     db.session.commit()
#     return user.id


class TestToken:
    def test_get_token(self, db, create_user):
        test_token = "my_token"
        token = Token(user_id=create_user.id, token=test_token)
        db.session.add(token)
        db.session.commit()

        assert Token.query.filter_by(token=test_token).first() is not None
        assert Token.query.filter_by(user_id=create_user.id).first().token == test_token
