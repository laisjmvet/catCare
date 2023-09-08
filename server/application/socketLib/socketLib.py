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
    before_answer()  
    session.modified = True 
    send_question()
    print("question sent!!!!!!!")

@socketio.on("disconnect")
def handle_disconnect():   
    print("User disconnected")

def send_question():    
    question = questionsLogic.sendQuestions()
    emit("question", question[0])

def before_answer():
    if "answers" not in session:
        session["answers"] = []  # Initialize the session variable if it doesn't exist
        session.modified = True


@socketio.on("answer")
def handle_answer(data):
    print(">>>>>>>>>>>>Received answer:", data)
    send_question()
