from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from . import bp
from ... import dbInterface, User
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

@bp.route("/event/createPost/<int:eventId>")
@login_required
def createPost(eventId):
    return render_template("events/createPost.html")


@bp.route('/event/createPost/<int:eventId>', methods=['POST'])
@login_required
def createPostSubmit(eventId):
    text = request.form['text']
    print(eventId)
    print(text)

    insert_query = "insert into eventPostings (eventID, ownerUsername, postContent) values (:eventID, :ownerUsername, :postContent)"
    insert_params = {
        "eventID": eventId,
        "ownerUsername": current_user.get_id(),
        "postContent": text
        }
    result = dbInterface.commit(insert_query, insert_params)

    return redirect("/event/" + str(eventId))


