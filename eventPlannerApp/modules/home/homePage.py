
from flask import render_template

from . import bp

@bp.route("/")
def homePageRoute():
    return render_template("home/homePage.html")
