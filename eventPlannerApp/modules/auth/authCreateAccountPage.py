from flask import render_template, request, redirect
from werkzeug.security import generate_password_hash
from ... import dbInterface
from . import bp

@bp.route("/signup")
def createAccountPageRoute():
    return render_template("auth/authCreateAccountPage.html")

@bp.route('/signup', methods=['POST'])
def createAccountSubmit():
    user = request.form['username']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    password = generate_password_hash(request.form['pass'], "sha256")
    associatedSchool = request.form['school']    

    insert_query = "insert into users values (:username, :firstName, :lastName, :password, :email, :associatedSchool)"
    insert_params = {
        "username": user,
        "firstName": firstName,
        "lastName": lastName,
        "password": password,
        "email": email,
        "associatedSchool": associatedSchool
        }
    result = dbInterface.commit(insert_query, insert_params)
    return redirect("/events")
    
