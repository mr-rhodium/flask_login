from extensions import db
import uuid
from extensions import bcrypt


class Token(db.Model):
    __tablename__ = "tokens"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    token = db.Column(db.String(255), nullable=True)
    user = db.relationship("User", backref="tokens")

    # def generate_token(self):
    #     self.token = str()

    @property
    def get_token(self):
        return self.token

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def __repr__(self):
        return f"<Token {self.id}>"
