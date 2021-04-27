from flask import Blueprint

bp = Blueprint('invitations', __name__)

from . import createInvitationPage
