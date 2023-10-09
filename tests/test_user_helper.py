from apps.user.helper import chek_token


def test_no_valid_token(client, db):
    resp = client.get("/user", headers={"x-access-token": "test"})
    assert resp.status_code == 404
    assert resp.json == {"message": "Token is invalid"}


def test_valid_token(client, create_token, data):
    resp = client.get("/user", headers={"x-access-token": create_token.token})
    assert resp.status_code == 200
    assert resp.json.get("name") == data["user"]["name"]
    assert resp.json.get("email") == data["user"]["email"]
