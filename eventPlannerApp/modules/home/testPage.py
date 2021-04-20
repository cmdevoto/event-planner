
from flask import render_template

from . import bp

@bp.route("/testDatabase")
def homePageRoute():
    return render_template("home/testPage.html")
