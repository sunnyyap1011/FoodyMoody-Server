from app import app
# from flask_cors import CORS
# from app import csrf

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from foody_api.blueprints.restaurants.views import restaurants_api_blueprint
from foody_api.blueprints.rooms.views import rooms_api_blueprint
from foody_api.blueprints.messages.views import messages_api_blueprint


app.register_blueprint(restaurants_api_blueprint, url_prefix='/api/v1/restaurants')
app.register_blueprint(rooms_api_blueprint, url_prefix='/api/v1/rooms')
app.register_blueprint(messages_api_blueprint, url_prefix='/api/v1/messages')

# csrf.exempt(restaurants_api_blueprint)
# csrf.exempt(rooms_api_blueprint)