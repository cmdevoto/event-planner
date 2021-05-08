from flask import render_template, request, redirect
from werkzeug.security import check_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required

@bp.route("/changePassword")
@login_required
def changePass():
    return render_template("auth/authChangePassword.html")


@bp.route('/changePassword', methods=['POST'])
def changePassSubmit():
    email = request.form['email']
    password = request.form['pass']
    username = request.form['username']    

    searchQuery = "select PASSWORDHASH from users where username = :username"
    searchParams = {
        "username": username
        }

    result = dbInterface.fetchOne(searchQuery, searchParams)
    if result:
        if(check_password_hash(result[0], password)):
            print("logged in")
            user = User.User()
            user.id = email
            login_user(user)
            return redirect("/test/databaseRetrieveItems")
        else:
            print("not logged in")
            return redirect("/login")
    else:
        print("not logged in")
        return redirect("/login")
