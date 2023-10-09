from flask import request

from flask import Blueprint, Response, jsonify, request
from apps.user.models import User
from apps.token.models import Token
from extensions import db
import json
import uuid
from flask import flash

from apps.user.helper import chek_email


auth_blueprint = Blueprint("Auth", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
    }

    data = request.get_json()

    name = data.get("name", False)
    email = data.get("email", False)
    password = data.get("password", False)

    if all([name, email, password]):
        if chek_email(email):
            return Response(
                json.dumps({"message": "user already exist"}),
                status=409,
                headers=headers,
            )
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        return Response(
            json.dumps({"message": "user created"}), status=201, headers=headers
        )

    return Response(
        json.dumps({"message": "user not created"}), status=404, headers=headers
    )


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", False)
    password = data.get("password", False)

    if all([email, password]):
        user = User.query.filter_by(email=email).first()
        if not user:
            return Response(
                json.dumps({"message": "user not found"}),
                status=403,
                headers={"Content-Type": "application/json"},
            )

        elif user.check_password(password):
            token = Token(user_id=user.id, token=str(uuid.uuid4()))
            db.session.add(token)
            db.session.commit()
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
                "x-access-token": token.get_token,
            }
            return Response(
                json.dumps({"message": "user logged in"}), status=200, headers=headers
            )

    return Response("Invalid data")
