class TestUserViews:
    def test_get_user_info(self, client, db, create_user, create_token, data):
        headers = {"x-access-token": data["token"]}
        response = client.get("/user", headers=headers)
        assert response.status_code == 200
        assert response.json.get("name") == data["user"]["name"]
        assert response.json.get("email") == data["user"]["email"]
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["Access-Control-Allow-Origin"] == "*"

    def test_get_user_info_by_id_not_found(self, client):
        response = client.get("/user")
        assert response.status_code == 404
        assert response.json == {"message": "User not found"}
