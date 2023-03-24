from controllers import user_controller
import db
import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__, instance_relative_config=True)
load_dotenv()
app.config.from_object(os.environ['APP_SETTINGS'])

# init db
db.init_app(app)

app.register_blueprint(user_controller.user_bp)

if __name__ == '__main__':
    app.run()
