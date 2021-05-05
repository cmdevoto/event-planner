from flask import Blueprint

bp = Blueprint('invitation', __name__)

from . import invitationHomePage
