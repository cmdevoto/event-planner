from flask import render_template, request
from werkzeug.security import generate_password_hash
import ~/event-planner/eventPlannerApp/dbInterface.py
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
    
    commit("insert into TABLE " + user + ", " + firstName + ", " + lastName + ", " + password + ", " + email, {})

    print(password)
    return render_template("home/homePage.html")
    
