import os
import sys
sys.path.append(str(os.path.dirname(os.path.abspath(__file__))))

# Application imports
import appointments
import binarySearchKernel
import diary
import diseases
import homepage
import login
import pets
import socketLib
import user
import user_answer_count
import variables
from db import *
from models import *

# Flask imports
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate  # db migration
from flask_session import Session

# Other imports
from dotenv import load_dotenv
load_dotenv()

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

    login.login_manager.init_app(app)
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
    socketLib.socket.socketio.init_app(app, cors_allowed_origins="*", manage_session=True)
    migrate.init_app(app, db)
    app.app_context().push()
    CORS(app, support_credentials=True)
 
    # Blueprints registration
    app.register_blueprint(user.user)
    app.register_blueprint(homepage.homepage)
    app.register_blueprint(login.auth)
    app.register_blueprint(appointments.appointment)
    app.register_blueprint(pets.pet)
    app.register_blueprint(diary.diary)
    app.register_blueprint(variables.variables)
    app.register_blueprint(user_answer_count.users_answers_count)
    app.register_blueprint(diseases.diseases)

    return app
