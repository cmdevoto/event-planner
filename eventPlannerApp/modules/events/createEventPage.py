from flask import redirect, render_template

from . import bp
from ... import dbInterface

@bp.route("/createevent")
def createEventPageRoute():
    resultingGroups = dbInterface.fetchAll("select * from groups", {})
    data = {
        "groups": resultingGroups
    }
    return render_template("events/createEvent.html", data=data)

"""
@bp.route("/createevent", methods=['POST'])
def createEventSubmit():
    
    desc = request.form['eventDesc']
    time = request.form['eventTime']
    loc = request.form['eventLocation']
    owner = request.form['eventOwner']
    groups = request.form['groupSelect']
    status = request.form['eventAccess']

    # must get username from the session
    # must get user's school from the session

    # many to many events to groups, will get the groups from the form and insert them into the new table

    eventInsertQuery = "insert into events values (:description, :eventTime, :location, :ownerUsername, :accessStatus, :associatedSchool, :creatorUsername)"
    
    groupInsertQuery = "insert into eventGroups values (:eventID, :groupID, :groupName)"

    eventInsertParams = {
        "description": desc,
        "eventTime": time,
        "location": loc,
        "ownerUsername": owner,
        "accessStatus": status,
        "associatedSchool":
        "creatorUsername":
    }

    result = dbInterface.commit(eventInsertQuery, eventInsertParams)

    # query to get eventID
    eventID = dbInterface.fetchOne("select eventID from events order by eventID desc limit 1", {})

    for n in groups:
        query = "select groupID from groups where groupName = (:name)"
        param = {
            "name": n
        }
    
        groupID = dbInterface.fetchOne(query, param)
        
        groupInsertParams = {
            "eventID": eventID
            "groupID": groupID,
            "groupName" : n
        }

    return redirect("events/eventHome.html")
"""

