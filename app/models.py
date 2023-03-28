from sqlalchemy import func
from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

saved_cars = db.Table("saved_cars",
                      db.Column('user_id', db.Integer, db.ForeignKey(
                          'user.id'), primary_key=True),
                      db.Column('car_id', db.Integer, db.ForeignKey(
                          'car.id'), primary_key=True)
                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150))
    cars = db.relationship('Car', backref='seller', lazy=True)
    saved_cars = db.relationship(
        "Car", secondary="saved_cars", backref="saved_by", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    mileage = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    posted_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
