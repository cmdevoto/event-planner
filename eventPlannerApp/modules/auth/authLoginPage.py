from flask import render_template

from . import bp

@bp.route("/login")
def hello_route():
    return render_template("auth/authLoginPage.html")
