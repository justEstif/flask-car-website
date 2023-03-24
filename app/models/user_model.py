from db import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)
