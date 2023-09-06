import os
import sys
from pathlib import Path
full_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(str(Path(full_path).parents[1]))
from flask_socketio import SocketIO

socketio = SocketIO()

@socketio.on("answer")
def handle_answer(data):
    print(">>>>>>>>>>>>Received answer:", data)


