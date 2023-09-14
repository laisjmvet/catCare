import os
import sys
from pathlib import Path
full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[1]))

from flask_socketio import SocketIO, emit
from application.binarySearchKernel.qaLogic import QALogic
from flask import session

socketio = SocketIO()

@socketio.on("connect")
def handle_connect():
    # before_answer()  
    session['data'] = []
    session['questionsIDs'] = []
    session.modified = True
    send_question([], [])
    print("question sent!!!!!!!")

@socketio.on("disconnect")
def handle_disconnect():   
    session.pop('data', None)
    session.pop('questionsIDs', None)
    print("User disconnected")

def send_question(userResponse, questionsIDs): 
    qaLogic = QALogic(15)   
    question = qaLogic.getDynamicQuestion(userResponse, questionsIDs) 
    print("question sent >>>>>", question)
    emit("question", question[0])

@socketio.on("answer")
def handle_answer(data):
    session['data'].append(data)
    session['questionsIDs'].append(data['questionID'])
    session.modified = True
    print("Answers: >>>>>>>>> ", session['data'], session['questionsIDs'])
    send_question(session['data'], session['questionsIDs'])
