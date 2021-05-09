from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")



    
