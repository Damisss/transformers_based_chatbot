from flask import Flask
from flask_cors import CORS

from config import Config 

def create_app(*, config_object:Config)-> Flask:
    flask_app = Flask('app')
    flask_app.config.from_object(config_object)
    CORS(flask_app)
    with flask_app.app_context():
        from controllers.core import app
        flask_app.register_blueprint(app)
    
    return flask_app

#resources={r"/api/*": {"origins": "*"}},  supports_credentials=True