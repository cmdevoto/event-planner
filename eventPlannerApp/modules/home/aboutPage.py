
from flask import render_template

from . import bp

@bp.route("/about")
def aboutPageRoute():
    return render_template("home/aboutPage.html")
