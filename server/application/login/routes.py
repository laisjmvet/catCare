from flask import Blueprint, request, jsonify, session
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask_bcrypt import check_password_hash
from login_manager import login_manager

auth = Blueprint("auth", __name__)


# Configure the user_loader callback to retrieve a user by ID
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Define the login route
@auth.route("/login", methods=["POST"])
def login():
    # Get email and password from the JSON payload
    email = request.json.get("email")
    password = request.json.get("password")
    # Query the User model for the provided email
    user = Users.query.filter_by(email=email).first()
    # Check if the user exists and the password is correct
    if check_password_hash(user.password, password):
        # Use the login_user function to log in the user
        login_user(user)
        # session['data'] = []
        # session.modified = True
        # answers = session.get('data')
        # if answers is not None:
        #     print(f'Answers received: {answers}')
        # else:
        #     print('No data in the session', 404 )
        return (
            jsonify(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user.password,
            ),
            200,
            )    
    
    # Return an error response if authentication fails
    return jsonify({"message": "Invalid email or password"}), 401

@auth.route('/logout', methods=['GET'])
def logout():
    # Clear session data    
    # print("logout", session['data'])
    # session.pop('data', None)
    # session.modified = True
    return jsonify({"message": "Logout successful"}), 200
