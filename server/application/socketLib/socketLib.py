import os
import sys
from pathlib import Path
full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[1]))

from flask_socketio import SocketIO, emit
from application.binarySearchKernel import questionsLogic

socketio = SocketIO()

@socketio.on("connect")
def handle_connect():
    print("question sent!!!!!!!")

def send_question():    
    question = questionsLogic.sendQuestions()
    emit("question", question[0])

@socketio.on("answer")
def handle_answer(data):
    print(">>>>>>>>>>>>Received answer:", data)
    send_question()
