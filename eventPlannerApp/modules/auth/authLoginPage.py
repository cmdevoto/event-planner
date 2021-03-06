from flask import render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager

@bp.route("/login")
def hello_route():
    return render_template("auth/authLoginPage.html")


@bp.route('/login', methods=['POST'])
def loginSubmit():
    password = request.form['pass']
    username = request.form['username']    

    searchQuery = "select PASSWORDHASH from users where username = :username"
    searchParams = {
        "username": username
        }

    result = dbInterface.fetchOne(searchQuery, searchParams)
    if result:
        if(check_password_hash(result[0], password)):
            user = User.User()
            user.id = username
            login_user(user)
            # must make this protected route
            return redirect("/events")
            #return redirect("/test/databaseRetrieveItems")
        else:
            flash("Incorrect Username or Password")
            return redirect("/login")
    else:
        return redirect("/login")
