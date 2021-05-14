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
    email = current_user.get_id()
    password = request.form['pass'] 

    searchQuery = "select PASSWORDHASH from users where email = :email"
    searchParams = {
        "email": email
        }

    result = dbInterface.fetchOne(searchQuery, searchParams)
    if result:
        if(check_password_hash(result[0], password)):
            print("password matches: proceed to deletion")
            
            deleteQuery = "delete from users where email = :email"
            deleteParams = {
                "email": email
                }

            result = dbInterface.commit(deleteQuery, deleteParams)
            print("deletion successful")
            flash("deletion successful")
            logout_user()
            return redirect("/login")
        else:
            print("passwords do not match")
            return redirect("/deleteAccount")
    else:
        print("no user found, fatal")
        return redirect("/login")

    
