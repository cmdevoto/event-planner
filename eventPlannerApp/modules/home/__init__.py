from flask import Blueprint

bp = Blueprint('home', __name__)

from . import homePage
from . import testPage
from . import aboutPage
