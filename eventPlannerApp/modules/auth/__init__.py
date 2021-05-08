from flask import Blueprint

bp = Blueprint('modules', __name__)

from . import authLoginPage
from . import authCreateAccountPage
from . import authChangePasswordPage
