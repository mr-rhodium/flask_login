from flask import Flask
from apps.auth.views import auth_blueprint
from apps.user.views import user_blueprint
from extensions import db, bcrypt, migrate


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)


def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
