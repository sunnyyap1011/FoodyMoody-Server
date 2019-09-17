from app import socketio
from flask_socketio import emit, send, join_room, leave_room, rooms
from flask import Blueprint, jsonify, request
import random

rooms_api_blueprint = Blueprint('rooms_api',
                             __name__,
                             template_folder='templates')


# @rooms_api_blueprint.route('/', methods=['GET'])
# def index():
#     return

rooms_list = []

def callback_response():
    return "Message was receive"

@socketio.on('connect')
def on_connect():
    # print(data.msg)
    print("Server's connect")
    emit("connected", {"msg": "I'm from server", "sid": request.sid}, broadcast=True)


@socketio.on('create_room')
def create_room():
    room_id = str(random.randint(1000,9999))
    rooms_list.append(room_id)
    join_room(room_id)
    print("Creating room")
    emit('get_room_id', {"room_id": room_id})
    emit('broadcast_rooms', {"rooms": rooms_list})


@socketio.on('join_room')
def join(data):
    room_id = data['room_id']
    if room_id in rooms_list:
        join_room(room_id)
        emit('broadcast_num_ppl', room=room_id)
        emit('check_room_exist', {"valid": True})
    else:
        emit('check_room_exist', {"valid": False})


@socketio.on('conditions')
def get_google_api(data):
    location = data['location']
    rounds = data['rounds']
    room = data['room']
    # get info from Google API 
    data = [
        {"name": "Restaurant 1", "rating": 4.9, "operating_hours": "9.00am - 5.00pm", "price": "$$$", "picture": "logo.img"},
        {"name": "Restaurant 2", "rating": 4.5, "operating_hours": "9.00am - 5.00pm", "price": "$$$", "picture": "logo.img"},
        {"name": "Restaurant 3", "rating": 4.6, "operating_hours": "9.00am - 5.00pm", "price": "$$$", "picture": "logo.img"},
        {"name": "Restaurant 4", "rating": 5.0, "operating_hours": "9.00am - 5.00pm", "price": "$$$", "picture": "logo.img"},
        {"name": "Restaurant 5", "rating": 4.9, "operating_hours": "9.00am - 5.00pm", "price": "$$$", "picture": "logo.img"},
    ]
    emit('check_start',  room=room)
    emit('broadcast_restaurants', data, room=room)


@socketio.on('total_ppl')
def total_ppl(data):
    emit('broadcast_total_ppl', {"num_ppl": data['num_ppl']}, room=data['room_id'])


@socketio.on('vote_A')
def vote_A(data):
    emit('broadcast_A_votes', room=data["room_id"])


@socketio.on('vote_B')
def vote_B(data):
    emit('broadcast_B_votes', room=data["room_id"])

@socketio.on('check_result')
def check_result(data):
    if data['A']['votes'] > data['B']['votes']:
        result = {
            "card": "A",
            "votes": data['A']['votes'],
            "restaurant_name": data['A']['restaurant_name']
        }
    else:
        result = {
            "card": "B",
            "votes": data['B']['votes'],
            "restaurant_name": data['B']['restaurant_name']
        }
    emit('broadcast_result', result, room=data['room_id'])


@socketio.on('disconnect')
def disconnect():
    print("One user disconnect")
    print(rooms()[1])
    emit('on_leave', room=rooms()[1])
