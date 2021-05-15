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
            flash("Incorrect Username or Password")
            return redirect("/login")
    else:
        print("not logged in")
        return redirect("/login")
