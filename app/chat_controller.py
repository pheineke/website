from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from flask_socketio import *

import json

from app.models.text_chat import Chat
from app.models.voice_chat import VoiceChat




chat = Blueprint('chat', __name__)

chat_handler = Chat()

@chat.route('/')
def index():

    return render_template('chat.html')

@chat.route('/rooms', methods=['GET'])
def rooms():

    room_count = chat_handler.get_room_count()

    return jsonify(room_count)

@chat.route('/room/<room_id>', methods=['GET'])
def history(room_id):
    if chat_handler.get_room_count() == 0:
        return jsonify({"no": "no"})
    else:
        data = chat_handler.get_messages(room=room_id)

        return jsonify(data)

@chat.route('/send/<room_id>', methods=['POST'])
def send(room_id):
    if chat_handler.get_room_count() == 0:
        return jsonify({"no": "no"})
    else:
        # Get the message from the request
        message = request.json

        user = message.get('user')
        content = message.get('content')

        data = chat_handler.add_message(room=room_id, user=user, content=content)

        return jsonify(data)

@chat.route('/create_text')
def create_chat_room():
    data = chat_handler.create_room()

    return jsonify(data)

#######

@socketio.on('audio_data')
def handle_audio(data):
    emit('audio_stream', data, broadcast=True)  # Broadcast to all connected clients


@chat.route('/create_voice')
def create_voice_room():
    data = chat_handler.create_voice_room()

    return jsonify(data)

