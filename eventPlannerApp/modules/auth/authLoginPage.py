from flask import render_template, request, redirect
from werkzeug.security import check_password_hash
from . import bp
from ... import dbInterface

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
    result = dbInterface.fetchOne(searchQuery, searchParams)
    print(email)
    print(password)
    print("Here is the password hash: ") 
    print(result)

    if(check_password_hash(result, password)):
        print("logged in")
    else:
        print("not logged in")

    return redirect("home/homePage.html")