from os import path, environ
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    with app.app_context():
        create_database()


def create_database():
    if not path.exists("instance/" + environ["DATABASE_NAME"]):
        db.create_all()
        print("Created Database!")

    print("Connected to Database!")


@contextmanager
def transaction():
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def persist(*args):
    db.session.add_all(args)


def delete(obj):
    db.session.delete(obj)


def execute(sql):
    return db.session.execute(sql)
