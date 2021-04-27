from flask import render_template, request, redirect
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
    result = dbInterface.fetchOne(searchQuery, searchParams)[0]

    if(check_password_hash(result, password)):
        print("logged in")
        user = User.User()
        user.id = username
        login_user(user)
    else:
        print("not logged in")

    return redirect("/test/databaseRetrieveItems")
