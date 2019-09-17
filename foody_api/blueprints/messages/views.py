from flask import Blueprint, jsonify, request
from app import socketio
from flask_socketio import emit, send

messages_api_blueprint = Blueprint('messages_api',
                             __name__,
                             template_folder='templates')


# @messages_api_blueprint.route('/', methods=['GET'])
# def index():
#     return



