from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")


@user_bp.route("/", methods=(["GET"]))
@login_required  # must be logged in to access
def home():
    return render_template("home.jinja2", user=current_user)
# save car
