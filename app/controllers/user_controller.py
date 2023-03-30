from flask import Blueprint, render_template, request
import requests
from flask_login import login_required, current_user
from models import Car
from flask_wtf import FlaskForm
from wtforms import (StringField,  PasswordField, )
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError
from db import db


user_bp = Blueprint("user_bp", __name__, url_prefix="/")


@user_bp.route("/", methods=(["GET", "POST"]))
@login_required  # must be logged in to access
def home():
    form = NewCarForm()
    if request.method == "POST":
        if form.is_submitted():
            new_car = Car(
                make=form.make.data,
                model=form.model.data,
                year=form.year.data,
                price=form.price.data,
                mileage=form.mileage.data,
                description=form.description.data,
                image_url=form.image_url.data,
                user_id=current_user.id,  # type: ignore
            )
            db.session.add(new_car)
            db.session.commit()

    cars = Car.query.order_by(Car.id.desc()).all()
    return render_template("home.jinja2", user=current_user, cars=cars, form=form)


class NewCarForm(FlaskForm):
    make = StringField("Make", validators=[DataRequired()])
    model = StringField("Model", validators=[DataRequired()])
    year = StringField("Year", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    mileage = StringField("Mileage", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    image_url = StringField("Image Url", validators=[DataRequired()])

    def validate_image_url(self, image_url):
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if not r.headers["content-type"] in image_formats:
            raise ValidationError("Image Url is not a valid image link.")
