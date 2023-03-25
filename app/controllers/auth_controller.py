from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user_model import User
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import (StringField,  PasswordField, )
from wtforms.validators import Email, DataRequired, EqualTo, Length, ValidationError

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("views.home"))  # redirect to home
    return render_template("login.jinja2", user=current_user, form=form)


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        return redirect(url_for("views.home"))  # redirect to home
    return render_template("sign_up.jinja2", user=current_user, form=form)


@auth_bp.route("/logout")
@login_required  # can't access page unless logged in
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(),
                                    Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(), Length(min=8, max=64)]
                             )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Incorrect email.")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if not check_password_hash(user.password, password.data):
                raise ValidationError("Incorrect password.")
            else:
                login_user(user, remember=True)


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=32)], )
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('Verify password',
                                     validators=[DataRequired(), EqualTo('password',
                                                                         message='Passwords must match')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is registered.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is registered.")

        else:
            new_user = User(
                email=self.email.data,
                username=self.username.data,
                password=generate_password_hash(
                    self.password.data, method="sha256"),
            )
            db.session.add(new_user)  # add created user to db
            db.session.commit()  # commit the current transaction
            login_user(new_user, remember=True)  # login user
