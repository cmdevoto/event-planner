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
    #password = generate_password_hash(request.form['pass'], "sha256")
    
    searchQuery = "select PASSWORDHASH from users where email = :email"
    searchParams = {
        "email": email
        }
    result = dbInterface.fetchOne(searchQuery, searchParams)
    print("Here is the password hash: " + result) 


    return redirect("home/homePage.html")