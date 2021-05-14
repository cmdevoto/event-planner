from flask import render_template, request, redirect, flash
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
    #print(event.split(':')[0])
    eventID = int(event.split(':')[0])

    inviterUsername = current_user.get_id()


    ### NEED TO CHECK IF USER CAN INVITE PEOPLE ###
    print("CREATE INVITE . PY")
    temp = dbInterface.fetchAll("select * from events where eventID = (:eventID)", {"eventID" : eventID})
    print(temp)
    accessType = temp[0][5]
    owner = temp[0][4]
    creator = temp[0][7]

    print(accessType)
    print(owner)
    print(creator)

    if accessType == "Private" or accessType == "private" and (owner != inviterUsername or creator != inviterUsername):
        print("you don't have permissions to invite others to this event")    
        flash("You do not have permission to invite others to this event.")
        return redirect("/createinvitation")


    # list of people invited
    inviteeUsernames = request.form.getlist('userSelect')
    
    # list of groups invited
    groups = request.form.getlist('groupSelect')
    groupID = []
    for g in groups:
        groupID.append(int(g.split(':')[0]))
        #groupID.append(int(g[0]))

    message = request.form['message']

    print(event, file=sys.stderr)
    print(eventID, file=sys.stderr)
    print(inviterUsername, file=sys.stderr)
    print(inviteeUsernames, file=sys.stderr)
    print(groups, file=sys.stderr)
    print(groupID, file=sys.stderr)
    print(message, file=sys.stderr)

    # make list of all people invited , only send one invitation to each person

    if inviteeUsernames:
        inviteSet = set(inviteeUsernames)
    else:
        inviteSet = set()   
    
    for gid in groupID:
        tempQuery = dbInterface.fetchAll("select * from groupMembership where groupID = (:groupID)", {"groupID" : gid})
        print(tempQuery)
        for t in tempQuery:
            inviteSet.add(t[0])
    print(inviteSet)

    # loop to make invitations (insert into eventInvitations)
    for i in inviteSet:
        inviteInsertQuery =  "insert into eventInvitations (eventID, inviterUsername, inviteeUsername, invitationMessage, status) values (:eventID, :inviterUsername, :inviteeUsername, :invitationMessage, :status)"
    
        inviteInsertParams = {
        "eventID": eventID,
        "inviterUsername": inviterUsername,
        "inviteeUsername": i,
        "invitationMessage": message,
        "status": "Pending"
        }
    
        result = dbInterface.commit(inviteInsertQuery, inviteInsertParams)

    return redirect("/invitations")
