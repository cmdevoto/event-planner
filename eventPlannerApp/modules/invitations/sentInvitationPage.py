from flask import render_template, request, redirect
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin

from . import bp
from ... import dbInterface
import sys

@bp.route("/sentinvitations")
def sentInvitationsPageRoute():
    resultingInvites = dbInterface.fetchAll("select * from eventInvitations where inviterUsername = (:iid)", {"iid" : current_user.get_id()})
    data = {
        "invitations": resultingInvites
    }
    #logout_user()
    print(current_user.get_id())
    print(resultingInvites)
    return render_template("invitations/sentInvitations.html", data=data)

@bp.route("/sentinvitations", methods=['POST'])
def rescindInvitationSubmit():
    print("pressed button")
    print(request.form)
    #print(request.form['eventID'])
    print(request.form['message'])
    return redirect("/sentinvitations")
