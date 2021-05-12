from flask import redirect, render_template
from flask_login import login_required

from . import bp
from ... import dbInterface

@login_required
@bp.route("/event/<int:eventId>")
def single_event_view_page(eventId):
    eventQuery = "select * from events where eventId=:eventId"
    eventQueryParams = {
      "eventId": 1
    }
    eventFromDb = dbInterface.fetchOne(eventQuery, eventQueryParams)

    event = {
      "name": eventFromDb[1],
      "timeDate": eventFromDb[2].strftime("%H:%M:%S, %m/%d/%Y"),
      "location": eventFromDb[3],
      "ownerUsername": eventFromDb[4],
      "ownerName": "",
      "accessType": eventFromDb[5],
      "associatedSchool": eventFromDb[6],
      "creatorUsername": eventFromDb[7],
      "creatorName": ""
    }

    print("Retrieving Event Id: {}".format(eventId))
    print("Raw Event: {}".format(eventFromDb))
    print("Event: {}".format(event))

    ownerQuery = "select firstname, lastname from users where username = :organizerUsername"
    ownerQueryParams = { "username": eventFromDb[4]}
    owner = dbInterface.fetchOne(ownerQuery, ownerQueryParams)
    event["ownerName"] = "{} {}".format(owner[0], owner[1])
    print("Raw Owner: {}".format(owner))
    
    if(event["ownerUsername"] != event["creatorUsername"]):
        creatorQuery = "select firstname, lastname from users where username = :creatorUsername"
        creatorQueryParams = { "username": eventFromDb[4]}
        creator = dbInterface.fetchOne(creatorQuery, creatorQueryParams)
        event["creatorName"] = "{} {}".format(creator[0], creator[1])
        print("Raw Creator: {}".format(owner))
    
    data = {
      "eventId": eventId,
      "event": event
    }
    return render_template("events/singleEventView.html", data=data)