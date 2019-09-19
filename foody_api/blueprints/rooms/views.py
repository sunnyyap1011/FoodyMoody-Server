from app import socketio
from flask_socketio import emit, send, join_room, leave_room, rooms
from flask import Blueprint, jsonify, request
import random
import requests
from config import Config
import os

rooms_api_blueprint = Blueprint('rooms_api',
                                __name__,
                                template_folder='templates')


rooms_list = []

details_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

photo_url = 'https://maps.googleapis.com/maps/api/place/photo'

key = Config.GOOGLE_API_KEY


def callback_response():
    return "Message was receive"


@socketio.on('connect')
def on_connect():
    print("Server's connect")
    emit("connected", {"msg": "I'm from server",
                       "sid": request.sid}, broadcast=True)


@socketio.on('create_room')
def create_room():
    room_id = str(random.randint(1000, 9999))
    rooms_list.append(room_id)
    join_room(room_id)
    print("Creating room")
    print(rooms_list)
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
    lat = str(data['lat'])
    lng = str(data['lng'])
    rounds = int(data['rounds'])
    room = data['room']
    # get info from Google API

    details_payload = {"key": key, "location": f"{lat},{lng}",
                       "radius": "1500", "types": ["restaurant", "food"]}

    details_resp = requests.get(details_url, params=details_payload)

    details_json = details_resp.json()

    results = details_json['results']

    results_rating = []

    for item in results:
        for each_key in item:
            if each_key == 'rating':
                results_rating.append(item)

    filtered_results_rating = list(
        filter(lambda x: x['user_ratings_total'] > 200, results_rating))

    sorted_results = sorted(filtered_results_rating,
                            key=lambda i: i['rating'], reverse=True)

    restaurants_list = []

    s = slice(rounds + 1)
    restaurants_list = sorted_results[s]

    for each in restaurants_list:
        photo_payload = {"key": key, "maxwidth": str(each['photos'][0]['width']), "photo_reference": each['photos'][0]['photo_reference']}

        photo_resp = requests.get(photo_url, params=photo_payload)

        each['photo_url'] = photo_resp.url


    data = [
        {"name": x['name'], "rating": x['rating'], "photo_url": x['photo_url'], "place_id": x['place_id'], "lat": x['geometry']['location']['lat'], "lng": x['geometry']['location']['lng']} for x in restaurants_list
    ]

    print(data)

    emit('check_start',  room=room)
    emit('broadcast_restaurants', data, room=room)


@socketio.on('total_ppl')
def total_ppl(data):
    emit('broadcast_total_ppl', {
         "num_ppl": data['num_ppl']}, room=data['room_id'])


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
    # print(rooms()[1])
    # print(rooms_list)
    emit('on_leave', room=rooms()[1])
