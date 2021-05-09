from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

@bp.route("/changePassword")
@login_required
def changePass():
    return render_template("auth/authChangePassword.html")


@bp.route('/changePassword', methods=['POST'])
def changePassSubmit():
    email = request.form['email']
    password1 = request.form['pass1']
    password2 = request.form['pass2']    

    if(password1 == password2):
        password = generate_password_hash(request.form['pass'], "sha256")
        updateQuery = "update users set PASSWORDHASH = :pass where email = :email"
        
        updateParams = {
            "email": email,
            "pass": password
        }

        result = dbInterface.commit(updateQuery, updateParams)
        flash("Please Log In Again")
        logout_user()
        return redirect("/login")
    else:
        flash("Passwords must match")
        return redirect("/changePassword")

    
