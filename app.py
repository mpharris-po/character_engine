from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def chat(msg):
    print(msg)

if __name__ == '__main__':
    socketio.run(app, debug=True)
