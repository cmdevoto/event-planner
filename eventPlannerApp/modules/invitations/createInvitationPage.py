from flask import render_template, request, redirect
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin

from . import bp
from ... import dbInterface
import sys

@bp.route("/createinvitation")
def createInvitationPageRoute():
    resultingEvents = dbInterface.fetchAll("select * from events", {})
    resultingUsers = dbInterface.fetchAll("select * from users", {})
    resultingGroups = dbInterface.fetchAll("select * from groups", {})
    data = {
        "events": resultingEvents,
        "users": resultingUsers,
        "groups": resultingGroups
    }
    #logout_user()
    print(current_user.get_id())
    return render_template("invitations/createInvitation.html", data=data)


@bp.route("/createinvitation", methods=['POST'])
def createInvitationSubmit():
    
    event = request.form['eventSelect']
    inviterUsername = current_user.get_id()
    
    # list of people invited
    inviteeUsernames = request.form.getlist('userSelect')
    
    # list of groups invited
    groups = request.form.getlist('groupSelect')

    message = request.form['message']
    status = 'Pending'

    print(event, file=sys.stderr)
    print(inviterUsername, file=sys.stderr)
    print(inviteeUsernames, file=sys.stderr)
    print(groups, file=sys.stderr)
    print(message, file=sys.stderr)
    print(status, file=sys.stderr)
   
    # must get event ID
    eventID = 0
    
    # must get group ID

    # make list of all people invited , only send one invitation to each person
   
    # select * from groupMembership where groupID = <groupID>
    # resultingUsersGroups = dbInterface.fetchAll("select * from groupMembership where groupID = (:groupID)", {"groupID" : groupID})
    # for entry in resultingUsersGroups:
        # if entry in inviteeUsernames:
            # continue
        #else:
            #inviteeUsernames.append(entry[0])


    inviteInsertQuery = "insert into eventInvitations (eventID, inviterUsername, inviteeUsername, invitationMessage, status) values (:eventID, :inviterUsername, :inviteeUsername, :invitationMessage, :status)"
    
    inviteInsertParams = {
        "eventID": eventID,
        "inviterUsername": inviterUsername,
        "inviteeUsername": inviteeUsername,
        "invitationMessage": message,
        "status": "Pending"
    }
    
    result = dbInterface.commit(inviteInsertQuery, inviteInsertParams)

    return redirect("/invitations")
