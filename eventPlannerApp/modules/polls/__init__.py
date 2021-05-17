from flask import Blueprint

bp = Blueprint('poll', __name__)

from . import pollHomePage
from . import createPoll
from . import myPolls
