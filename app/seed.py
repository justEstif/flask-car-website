import json
from db import db
from werkzeug.security import generate_password_hash


def seed_users():
    from models import User
    f = open("user.json")

    users = json.load(f)

    for user in users:

        new_user = User(
            username=user["username"],
            email=user['email'],
            password_hash=generate_password_hash(
                'testpassword', method="sha256"),
        )
        db.session.add(new_user)  # add created user to db
        db.session.commit()  # commit the current transaction

    print("Finished seeding users")
    f.close()


def seed_cars():
    from models import Car
    f = open("car.json")

    cars = json.load(f)

    for car in cars:
        new_car = Car(
            make=car["make"],
            model=car["model"],
            year=car["year"],
            price=car["price"],
            mileage=car["milage"],
            description=car["description"],
            image_url=car["image_url"],
            user_id=car["user_id"],
        )
        db.session.add(new_car)
        db.session.commit()
    print("Finished seeding cars")

    f.close()
