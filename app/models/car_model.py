from sqlalchemy import func
from db import db


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
