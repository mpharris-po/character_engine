from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from character import Character
from dotenv import load_dotenv

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def chat(msg):

    char = Character(name=msg.get("character"))

    resp = char.chat(msg.get("message_text"))

    emit("response", {"message": resp})

if __name__ == '__main__':
    load_dotenv()
    socketio.run(app, debug=True)
