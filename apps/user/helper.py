import json
from flask import request, Response
from functools import wraps
from apps.token.models import Token
from apps.user.models import User


def chek_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    return False


def chek_token(func):
    @wraps(func)
    def wrap():
        token = None
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        }
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if token:
            db_token = Token.query.filter_by(token=token).first()
            if db_token:
                return func(token)

            response_obj = {"message": "Token is invalid"}

            return Response(json.dumps(response_obj), status=404, headers=headers)

        else:
            response_obj = {"message": "User not found"}
            return Response(json.dumps(response_obj), status=404, headers=headers)

    return wrap
