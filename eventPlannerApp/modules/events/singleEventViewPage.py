from flask import redirect, render_template
from flask_login import login_required

from . import bp
from ... import dbInterface

@login_required
@bp.route("/event/<int:eventId>")
def single_event_view_page(eventId):
    eventFromDb = dbInterface.fetchOne("select * from events", {})
    event = {
      "name": eventFromDb[1],
      "timeDate": eventFromDb[2].strftime("%H:%M:%S, %m/%d/%Y"),
      "location": eventFromDb[3],
      "ownerUsername": eventFromDb[4],
      "accessType": eventFromDb[5],
      "associatedSchool": eventFromDb[6],
      "creatorUsername": eventFromDb[7]
    }
    print("Event Page: {}".format(event))
    data = {
      "eventId": eventId,
      "event": event
    }
    return render_template("events/singleEventView.html", data=data)