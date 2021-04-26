# Python packages
import os

# Flask packages
from flask              import Flask
from flask_session      import Session
from flask_login        import login_required, current_user, login_user, logout_user

# App packages
from . import config, dbInterface
from .modules import auth, home

os.environ["LD_LIBRARY_PATH"]="/u01/app/oracle/product/11.2.0/xe/lib"

def create_app():

    # Create app object
    application = Flask(__name__)

    #divs fucking with login stuff
    login.init_app(application)
    login.login_view = 'loginSubmit'

    # Config
    application.config.from_object(config.DefaultConfig)

    with application.app_context():
        # DB Interface blueprint
        application.register_blueprint(dbInterface.bp)
        # Module blueprints
        application.register_blueprint(modules.auth.bp)
        application.register_blueprint(modules.home.bp)

    return application
