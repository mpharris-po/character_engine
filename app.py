from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return "Welcome to the chat endpoint!"

if __name__ == '__main__':
    app.run(debug=True)
