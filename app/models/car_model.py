from sqlalchemy import func
from ..db import db


class Note(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # relation
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("notes", lazy=True))

    def __repr__(self) -> str:
        return f"Note('{self.user_id}', '{self.user}', '{self.data}', '{self.date}')"
