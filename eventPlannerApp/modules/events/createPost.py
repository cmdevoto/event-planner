from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

@bp.route("/events/createPost/<int:eventId>")
@login_required
def createPost(eventId):
    return render_template("events/createPost.html")


@bp.route('/events/createPost/<int:eventId>', methods=['POST'])
@login_required
def createPostSubmit(eventId):
    text = request.form['text']
    print(eventId)
    print(text)
    return redirect("/events/createPost/" + eventId)



    username = current_user.get_id()
    print("this is the userid")
    print(username)
    password1 = request.form['pass1']
    password2 = request.form['pass2']    

    if(password1 == password2):
        print("passwords match")
        passwordNew = generate_password_hash(password1, "sha256")
        updateQuery = "update users set PASSWORDHASH = :pass where username = :username"
        
        updateParams = {
            "username": username,
            "pass": passwordNew
        }

        result = dbInterface.commit(updateQuery, updateParams)
        print("Please Log In Again")
        flash("Password updated, please log in again!")
        logout_user()
        return redirect("/login")
    else:
        print("Passwords must match")
        flash("Passwords Must Match, Please Try Again!")
        return redirect("/changePassword")

    
