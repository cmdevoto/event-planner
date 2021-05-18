from flask import render_template, request, redirect
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface
import sys


@bp.route("/createevent")
@login_required
def createEventPageRoute():
    resultingGroups = dbInterface.fetchAll("select * from groups", {})
    data = {
        "groups": resultingGroups
    }
    #logout_user()
    return render_template("events/createEvent.html", data=data)


@bp.route("/createevent", methods=['POST'])
def createEventSubmit():
    
    desc = request.form['eventDesc']
    time = request.form['eventTime']
    loc = request.form['eventLocation']
    owner = request.form['eventOwner']
    groups = request.form.getlist('groupSelect')
    status = request.form['eventAccess']

    creatorUsername = current_user.get_id()
    associatedSchool = dbInterface.fetchOne("select associatedSchool from users where username = (:username)", {"username": creatorUsername})    

    # many to many events to groups, will get the groups from the form and insert them into the new table

    # NOTE: when inserting into events, groups, eventPostings, you must specify the column names bc it gets confused with the seq/trigger
    eventInsertQuery = "insert into events (description, eventTime, location, ownerUsername, accessStatus, associatedSchool, creatorUsername) values (:description, :eventTime, :location, :ownerUsername, :accessStatus, :associatedSchool, :creatorUsername)"
    
    groupInsertQuery = "insert into eventGroups values (:eventID, :groupID, :groupName)"

    eventInsertParams = {
        "description": desc,
        "eventTime": time,
        "location": loc,
        "ownerUsername": owner,
        "accessStatus": status,
        "associatedSchool": associatedSchool[0],
        "creatorUsername": creatorUsername
    }

    # kept getting an error and it sounds like its a bug on oracles part, just need to make sure that the session is altered
    timeAlter = dbInterface.commit("ALTER SESSION SET NLS_DATE_FORMAT = 'MM/DD/YYYY HH24:MI:SS'", {})
    result = dbInterface.commit(eventInsertQuery, eventInsertParams)

    # query to get eventID
    eventID = dbInterface.fetchOne("select eventID from events where rownum = 1 order by eventID desc", {})
    
    for n in groups:
        # this returns a tuple, must do [0]
        # also we'll need this to be unique, we can talk about that later
        groupID = dbInterface.fetchOne("select groupID from groups where groupName = (:name)", {"name": n})
        
        groupInsertParams = {
            "eventID": eventID[0],
            "groupID": groupID[0],
            "groupName" : n
        }
    
        groupResult = dbInterface.commit(groupInsertQuery, groupInsertParams)
    
    return redirect("/events")
