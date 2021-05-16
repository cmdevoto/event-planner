from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface

@bp.route("/invitations")
@login_required
def invitationHomePageRoute():
    resultingInvites = dbInterface.fetchAll("select * from eventInvitations where inviteeUsername = (:iid) and status = 'Pending'", {"iid" : current_user.get_id()})
 
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

    return render_template("invitations/invitationHome.html", data=data)

@bp.route("/invitations", methods=['POST'])
def acceptInvitationSubmit():
    print("pressed accept")

    try:
        eventID = request.args.get('eventID')
        inviterUsername = request.args.get('inviterUsername')
        inviteeUsername = current_user.get_id()
    except:
        flash("An error occured processing your request.")
        return redirect("/invitations")


    print("eventID = {}, inviterUsername = {}, inviteeUsername = {}".format(eventID, inviterUsername, inviteeUsername))

    acceptQuery = "update eventInvitations set status = 'Accepted' where eventID = (:eventID) and inviterUsername = (:inviterUsername) and inviteeUsername = (:inviteeUsername)"    
    queryParams = {
        "eventID": eventID,
        "inviterUsername": inviterUsername,
        "inviteeUsername":inviteeUsername
    }

    result = dbInterface.commit(acceptQuery, queryParams)
    flash('You successfully accepted this invitation')
    print(result)
    return redirect("/invitations")
