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
    
    searchQuery = "select PASSWORDHASH from users where email = :email"
    searchParams = {
        "email": email
        }
    result = dbInterface.fetchOne(searchQuery, searchParams)[0]

    if(check_password_hash(result, password)):
        print("logged in")
        user = User()
        user.id = email
        flask_login.login_user(user)
    else:
        print("not logged in")

    return redirect("home/homePage.html")