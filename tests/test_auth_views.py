from apps.user.models import User


class TestAuth:
    def test_register(self, client, db, data):
        response = client.post(
            "/register",
            json={
                "name": data["user"]["name"],
                "email": data["user"]["email"],
                "password": "123344",
            },
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 201
        user = User.query.filter_by(email=data["user"]["email"]).first()
        assert user is not None
        assert response.json["message"] == "user created"
        assert data["user"]["email"] == user.email
        assert data["user"]["name"] == user.name

    def test_no_valid_register(self, client, db):
        response = client.post(
            "/register",
            json={"name": "Ivan", "email": "", "password": "123344"},
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 404
        assert response.json["message"] == "user not created"

    def test_duble_register(self, client, db):
        response = client.post(
            "/register",
            json={"name": "Ivan", "email": "madn@majin.ddd", "password": "123344"},
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 201
        assert response.json["message"] == "user created"
        response_two = client.post(
            "/register",
            json={"name": "Ivan", "email": "madn@majin.ddd", "password": "123344"},
            headers={"Content-Type": "application/json"},
        )
        assert response_two.status_code == 409
        assert response_two.json["message"] == "user already exist"

    def test_login(self, client, db, create_user, data):
        response = client.post(
            "/login",
            json={"email": data["user"]["email"], "password": data["user"]["password"]},
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
        assert response.json["message"] == "user logged in"
        assert response.headers["x-access-token"] is not None

    def test_no_valid_login(self, client, db):
        response = client.post(
            "/login",
            json={"name": "Ivan", "email": "madn@majin.ddd", "password": "123344"},
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 403
        assert response.json["message"] == "user not found"
