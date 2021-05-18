from flask import render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

@bp.route("/deleteAccount")
@login_required
def deleteAccount():
    return render_template("auth/authDeleteAccount.html")


@bp.route('/deleteAccount', methods=['POST'])
@login_required
def deleteAccountSubmit():
    username = current_user.get_id()
    password = request.form['pass'] 

    searchQuery = "select PASSWORDHASH from users where username = :username"
    searchParams = {
        "username": username
        }

    result = dbInterface.fetchOne(searchQuery, searchParams)
    if result:
        if(check_password_hash(result[0], password)):
            #print("password matches: proceed to deletion")
            
            deleteQuery = "delete from users where username = :username"
            deleteParams = {
                "username": username
                }

            result = dbInterface.commit(deleteQuery, deleteParams)
            flash("Successfully Deleted Your Account!")
            logout_user()
            return redirect("/login")
        else:
            flash("The Pasword You Entered Does Not Match")
            return redirect("/deleteAccount")
    else:
        flash("No User FOund, Fatal")
        return redirect("/login")

    
