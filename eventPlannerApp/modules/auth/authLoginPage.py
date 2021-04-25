from flask import render_template
from werkzeug.security import check_password_hash
from . import bp

@bp.route("/login")
def hello_route():
    return render_template("auth/authLoginPage.html")
