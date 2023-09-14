from flask import Blueprint, request, jsonify, session
from application.models import Variables, db
variables = Blueprint("variables", __name__)


# Create a new variable
@variables.route("/variables", methods=["POST"])
def create_variable():
    data = request.json
    new_variable = Variables(
        specialty=data["specialty"],
        feature=data["feature"],
        question=data["question"],
        defaultQuestion=data["defaultQuestion"],
    )
    db.session.add(new_variable)
    db.session.commit()
    return jsonify({"message": "Variable created successfully!"}), 201


# Retrieve a variable by ID
@variables.route("/variables/<id>", methods=["GET"])
def get_variable_by_id(id):
    variable = Variables.query.get_or_404(id)
    variable_data = {
        "id": variable.id,
        "specialty": variable.specialty,
        "feature": variable.feature,
        "question": variable.question,
        "defaultQuestion": variable.defaultQuestion,
    }
    return jsonify(variable_data), 200


# @variables.route("/variables_questions", methods=["GET"])
# def get_variables_questions():    
#     questions = sendQuestions()    
#     return jsonify(questions), 200

# @variables.route("/variables/display_qa", methods=["GET"])
# def display_qa():
#     answers = session['data']
#     if answers is not None:
#         return f'Answers received: {answers}'
#     else:
#         return 'No data in the session', 404 

# @variables.route('/variables/set_session')
# def set_session():
#     session['username'] = 'JohnDoe'
#     return 'Session variable set'

# @variables.route('/variables/get_session')
# def get_session():
#     username = session.get('username', 'Guest')
#     return f'Hello, {username}'
