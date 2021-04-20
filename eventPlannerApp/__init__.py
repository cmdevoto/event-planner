# Python packages
import os

# Flask packages
from flask              import Flask
from flask_session      import Session

session = Session()

# App packages
from . import config, dbInterface
from .modules import auth, home

def create_app():

    # Create app object
    application = Flask(__name__)

    # Config
    application.config.from_object(config.DefaultConfig)

    with application.app_context():
        # DB Interface blueprint
        application.register_blueprint(dbInterface.bp)
        # Module blueprints
        application.register_blueprint(modules.auth.bp)
        application.register_blueprint(modules.home.bp)

    return application
