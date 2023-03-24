from flask import Blueprint

user_bp = Blueprint("user_bp", __name__, url_prefix="/user")


@user_bp.route("/", methods=(["GET"]))
def index():
    return "index"
