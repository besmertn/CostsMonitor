from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields

from src import db
from .entity import Entity


class User(Entity):
    __tablename__ = 'users'

    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password, created_by):
        Entity.__init__(self, created_by)
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if not self.password:
            return None
        return check_password_hash(self.password, password)


class UserShcema(Schema):
    id = fields.Number()
    username = fields.Str()
    password = fields.Str()
