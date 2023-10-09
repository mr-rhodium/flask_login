from flask import Blueprint, Response
from apps.user.helper import chek_token
from apps.user.models import User
from apps.token.models import Token
from extensions import db
import json


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/user", methods=["GET"])
@chek_token
def user_info(token):
    user_info = (
        Token.query.filter_by(token=token)
        .options(db.joinedload(Token.user, innerjoin=True))
        .first()
    )
    name = user_info.user.name
    email = user_info.user.email
    return Response(
        json.dumps({"name": name, "email": email}),
        status=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
    )
