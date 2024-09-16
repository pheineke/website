from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import json


chat = Blueprint('chat', __name__)

@chat.route('/')
def index():
    return render_template('chat.html')

@chat.route('/rooms', methods=['GET'])
def rooms():
    # Get count of rooms
    with open('chat.json', 'r') as f:
        data = json.load(f)
        room_count = data.get('room_count')
        print(room_count)
    return jsonify(room_count)

@chat.route('/<room_id>', methods=['GET'])
def history(room_id):
    # Get the chat history for the room
    data = get_history(room_id)

    return jsonify(data)

@chat.route('/send/<room_id>', methods=['POST'])
def send(room_id):
    # Get the message from the request
    message = request.json

    # Get the chat history for the room
    data = get_history(room_id)

    # Add the new message to the chat history
    data.append(message)

    # Save the chat history
    save_history(room_id, data)

    return jsonify(data)

def create_room():
    with open('chat.json', 'r') as f:
        data = json.load(f)
        room_id = data.get('room_count') + 1
        room = {
            'room_id': room_id,
            'messages': []
        }
        data.append(room)
        data['room_count'] += 1

    with open('chat.json', 'w') as f:
        json.dump(data, f)
    return room_id

def get_history(room_id):
    with open('chat.json', 'r') as f:
        data = json.load(f)
        room_data = data.get('room_data')
        for room in room_data:
            if int(room['room_id']) == int(room_id):
                return room['messages']
            
def save_history(room_id, data):
    with open('chat.json', 'r') as f:
        data = json.load(f)
        room_data = data.get('room_data')
        for room in room_data:
            if int(room['room_id']) == int(room_id):
                room['messages'] = data
                break
    with open('chat.json', 'w') as f:
        json.dump(data, f, indent=4)
    return data