from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash
from . import bp

from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager


@bp.route("/signup")
def createAccountPageRoute():
    return render_template("auth/authCreateAccountPage.html")

@bp.route('/signup', methods=['POST'])
def createAccountSubmit():
    username = request.form['username']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    password = generate_password_hash(request.form['pass'], "sha256")
    associatedSchool = request.form['school']    

    insert_query = "insert into users values (:username, :firstName, :lastName, :password, :email, :associatedSchool)"
    insert_params = {
        "username": username,
        "firstName": firstName,
        "lastName": lastName,
        "password": password,
        "email": email,
        "associatedSchool": associatedSchool
        }
    result = dbInterface.commit(insert_query, insert_params)
    user = User.User()
    user.id = username
    login_user(user)    

    return redirect("/events")
    
