from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

@bp.route("/editAccount")
@login_required
def editAccount():
    return render_template("auth/authEditAccount.html")




    
