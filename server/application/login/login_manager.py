# methods from Flask-Login for session management.
from flask_login import LoginManager

# create a flask_login instance
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
