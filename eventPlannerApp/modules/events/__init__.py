from flask import Blueprint

bp = Blueprint('event', __name__)

from . import eventHomePage
from . import createEventPage
from . import findEventsPage
