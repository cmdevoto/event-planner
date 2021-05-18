from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface
import sys

@bp.route("/sentinvitations")
@login_required
def sentInvitationsPageRoute():
    resultingInvites = dbInterface.fetchAll("select * from eventInvitations where inviterUsername = (:iid) and status = 'Pending'", {"iid" : current_user.get_id()})
    inviteInfo = []
    for i in resultingInvites:
        eventInfo = dbInterface.fetchOne("select * from events where eventID = (:id)", {"id" : i[0]})
        inviteInfoDict = {}
        inviteInfoDict = {
            "eventID": i[0],
            "inviterUsername" : i[1],
            "inviteeUsername" : i[2],
            "message" : i[3],
            "status" : i[4],
            "eventDesc" : eventInfo[1],
            "eventTime" : eventInfo[2],
            "eventLoc" : eventInfo[3]
        }
        inviteInfo.append(inviteInfoDict)
    data = {
        "invitations": resultingInvites,
        "invitationInfo" : inviteInfo
    }
    return render_template("invitations/sentInvitations.html", data=data)

@bp.route("/sentinvitations", methods=['POST'])
def rescindInvitationSubmit():

    try:
        eventID = request.args.get('eventID')
        inviteeUsername = request.args.get('inviteeUsername')
        inviterUsername = current_user.get_id()
    except:
        flash("An error occured while trying to process your request.")
        return redirect("/sentinvitations")

    
    deleteQuery = "delete from eventInvitations where eventID = (:eventID) and inviterUsername = (:inviterUsername) and inviteeUsername = (:inviteeUsername)"
    queryParams = {
        "eventID": eventID,
        "inviterUsername": inviterUsername,
        "inviteeUsername":inviteeUsername
    }
    result = dbInterface.commit(deleteQuery, queryParams)
    flash('You successfully rescinded this invitation.')
    return redirect("/sentinvitations")
