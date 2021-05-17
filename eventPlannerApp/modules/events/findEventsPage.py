from datetime import date
from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface

@bp.route("/findevents")
@login_required
def findEventsPageRoute():
    today = date.today()
    formattedToday = today.strftime("%d-%b-%y")
    resultingEvents = dbInterface.fetchAll("select * from events where eventtime > (:today) and (accessStatus = (:status) and ownerUsername != (:uname) and creatorUsername != (:uname) and eventID not in (select eventID from eventInvitations where inviteeUsername = (:uname)))", {"status": "Public", "uname": current_user.get_id(), "today" : formattedToday})

    data = {
        "events": resultingEvents
    }
    return render_template("events/findEvents.html", data=data)

@bp.route("/findevents", methods=['POST'])
def registerEventPageRoute():
    print("pressed register")
    
    try:
        eventID = request.args.get('eventID')
        inviteeUsername = current_user.get_id()
        inviterUsername = current_user.get_id()
    except:
        flash("An error occured processing your request.")
        return redirect("/invitations")

    inviteInsertQuery =  "insert into eventInvitations (eventID, inviterUsername, inviteeUsername, invitationMessage, status) values (:eventID, :inviterUsername, :inviteeUsername, :invitationMessage, :status)"
    
    inviteInsertParams = {
        "eventID": eventID,
        "inviterUsername": inviterUsername,
        "inviteeUsername": inviteeUsername,
        "invitationMessage": "",
        "status": "Accepted"
    }

    result = dbInterface.commit(inviteInsertQuery, inviteInsertParams)

    return redirect("/events")



