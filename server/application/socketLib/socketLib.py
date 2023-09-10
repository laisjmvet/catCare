import os
import sys
from pathlib import Path
full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[1]))

from flask_socketio import SocketIO, emit
from application.binarySearchKernel import questionsLogic
from flask import session
# from flask import request

socketio = SocketIO()

@socketio.on("connect")
def handle_connect():
    # before_answer()  
    session['data'] = []
    session['questionsIDs'] = []
    session.modified = True
    send_question()
    print("question sent!!!!!!!", session['data'], session['questionsIDs'])

# def before_answer():
#     if "data" not in session:
#         session['data'] = []  # Initialize the session variable if it doesn't exist
        # session.modified = True

@socketio.on("disconnect")
def handle_disconnect():   
    session.pop('data', None)
    session.pop('questionsIDs', None)
    print("User disconnected")

def send_question():    
    question = questionsLogic.sendQuestions()    
    emit("question", question[0])

@socketio.on("answer")
def handle_answer(data):
    # answer = data.get("answer")
    
    session['data'].append(data)
    session['questionsIDs'].append(data['questionID'])
    session.modified = True
    print(session['data'], session['questionsIDs'])
    print(">>>>>>>>>>>>Received answer:", data)
    send_question()
