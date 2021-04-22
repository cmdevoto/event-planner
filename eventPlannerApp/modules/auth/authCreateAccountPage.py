from flask import render_template

from . import bp

@bp.route("/signup")
def createAccountPageRoute():
    return render_template("auth/authCreateAccountPage.html")
