from app import app
# from flask_cors import CORS
# from app import csrf

# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from foody_api.blueprints.rooms.views import rooms_api_blueprint


app.register_blueprint(rooms_api_blueprint, url_prefix='/api/v1/rooms')
