from flask import redirect, render_template

from . import bp
from ... import dbInterface

@bp.route("/events")
def eventHomePageRoute():
    # will have to something along the lines of:
    # select  * from events where event_id in (select event_id from eventInvitations where inviteeUsername = <user> and status = 'accepted') or eventOwner = <user> or eventCreator = <user>

    resultingEvents = dbInterface.fetchAll("select * from events", {})
    data = {
        "events": resultingEvents
    }
    return render_template("events/eventHome.html", data=data)
