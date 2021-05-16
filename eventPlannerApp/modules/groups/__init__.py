from flask import Blueprint

bp = Blueprint('group', __name__)

from . import groupHomePage
from . import createGroupPage
from . import sendGroupInvitationPage
from . import viewGroupInvitationPage
