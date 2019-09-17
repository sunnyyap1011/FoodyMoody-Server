import os
import config
from flask import Flask, render_template
from config import Config
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
# from flask_wtf.csrf import CSRFProtect
# from flask_jwt_extended import JWTManager
# from flask_login import LoginManager
# from models.base_model import db
# import boto3, botocore
# import braintree
app = Flask('FOODY')

app.secret_key = Config.SECRET_KEY

socketio = SocketIO(app)

CORS(app)

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

# login_manager = LoginManager()
# login_manager.init_app(app)

# csrf = CSRFProtect(app)

# jwt = JWTManager(app)

# s3 = boto3.client(
#    "s3",
#    aws_access_key_id=Config.S3_KEY,
#    aws_secret_access_key=Config.S3_SECRET
# )

# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         braintree.Environment.Sandbox,
#         merchant_id=Config.BRAINTREE_MERCHANT_ID,
#         public_key=Config.BRAINTREE_PUBLIC_KEY,
#         private_key=Config.BRAINTREE_PRIVATE_KEY
#     )
# )

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


# @app.before_request
# def before_request():
#     db.connect()


# @app.teardown_request
# def _db_close(exc):
#     if not db.is_closed():
#         print(db)
#         print(db.close())
#     return exc
