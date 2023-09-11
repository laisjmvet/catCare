""" application factory 
function to call with diff setting (dev or testing environment)
run different version of the app (multiple instances with different config)
setup app factory """
from flask import Flask, session
from flask_cors import CORS
import os  # inbuilt python module
from dotenv import load_dotenv
from .db import db
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate  # db migration
from application.socketLib import socketLib
from flask_session import Session

load_dotenv()

# methods from Flask-Login for session management.
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

# create a flask_login instance
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# create an instance of SQLAlchemy, Migrate, and Bcrypt.

migrate = Migrate()
bcrypt = Bcrypt()
sessionConfig = Session()

def create_app(env=None):
    # initialise the app
    app = Flask(__name__)
    # Flask instance
    app.secret_key = "secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False    # Session will expire when the browser is closed
    app.config['SESSION_USE_SIGNER'] = True  # Enable cookie signing
    app.config['SESSION_KEY_PREFIX'] = 'your_prefix'  # Set a unique prefix

    login_manager.init_app(app)
    bcrypt.init_app(app)

    # config setup for different environment
    if env == "TEST":
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        app.config["SECRET_KEY"] = "test"
    else:  # development
        app.config["TESTING"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
        app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    # initialising the db and connecting to app
    db.init_app(app)
    sessionConfig.init_app(app)
    socketLib.socketio.init_app(app, cors_allowed_origins="*", manage_session=True)
    migrate.init_app(app, db)
    app.app_context().push()
    CORS(app, support_credentials=True)

    # BLUEPRINTS
    from application.homepage.routes import homepage
    from application.login.routes import auth
    from application.appointments.routes import appointment
    from application.user.routes import user
    from application.pets.routes import pet

    from application.diary.routes import diary
    from application.variables.routes import variables
    from application.user_answer_count.routes import users_answers_count
    from application.diseases.routes import diseases

    # Blueprints registration
    app.register_blueprint(user)
    app.register_blueprint(homepage)
    app.register_blueprint(auth)
    app.register_blueprint(appointment)
    app.register_blueprint(pet)
    app.register_blueprint(diary)
    app.register_blueprint(variables)
    app.register_blueprint(users_answers_count)
    app.register_blueprint(diseases)

    return app
