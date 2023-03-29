import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
import db
from controllers import user_controller, auth_controller

app = Flask(__name__, instance_relative_config=True)
load_dotenv()
app.config.from_object(os.environ['APP_SETTINGS'])

# init db
db.init_app_db(app)

# with app.app_context():
#     from seed import seed_cars, seed_users
#     seed_users()
#     seed_cars()


app.register_blueprint(user_controller.user_bp)
app.register_blueprint(auth_controller.auth_bp)

# setup login manager
login_manager = LoginManager()
login_manager.login_view = "auth_bp.login"  # type: ignore
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    from models import User
    return User.query.get(
        int(id)
    )  # look for the primary key and check if it matches id


if __name__ == '__main__':
    app.run()
