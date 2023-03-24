from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user_model import User
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("User logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))  # redirect to home
            else:
                flash("Wrong password, try again", category="error")

        else:
            flash("User doesn't exist", category="error")

    return render_template("login.html", user=current_user)


@auth_bp.route("/logout")
@login_required  # can't access page unless logged in
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()

        if user:
            flash("User with email already exists", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
        elif len(name) < 2:
            flash("First Name must be greater than 2 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        elif len(password1) < 7:
            flash("Password must be greater than 7 characters", category="error")
        else:
            # create user with hashed password
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)  # add created user to db
            db.session.commit()  # commit the current transaction
            flash("Account created", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))  # redirect to home
    return render_template("sign_up.html", user=current_user)
