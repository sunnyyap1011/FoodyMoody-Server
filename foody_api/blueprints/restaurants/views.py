from flask import Blueprint, jsonify, request

restaurants_api_blueprint = Blueprint('restaurants_api',
                             __name__,
                             template_folder='templates')


# @restaurants_api_blueprint.route('/', methods=['GET'])
# def index():
#     return