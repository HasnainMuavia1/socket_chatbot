from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from groq import Groq
client = Groq(api_key='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')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('client_message')
def handle_message(message):
    print('Received message from client:', message)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful Networking Assistant"
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": message
            }
        ],

        # The language model which will generate the completion.
        model="llama3-8b-8192",
        temperature=0.3,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    response = chat_completion.choices[0].message.content
    # Broadcast the message to all clients (including sender)
    emit('server_response', {'msg': response}, broadcast=True)


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('server_response', {'msg': 'Welcome to the chat!'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
