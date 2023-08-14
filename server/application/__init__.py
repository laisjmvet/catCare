from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os  # inbuilt python module

""" application factory 
function to call with diff setting (dev or testing environment)
run different version of the app (multiple instances with different config)
setup app factory """

# create an instance of the db
db = SQLAlchemy()


def create_app(env=None):
    # initialise the app
    app = Flask(__name__)
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
    app.app_context().push()
    CORS(app)

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
