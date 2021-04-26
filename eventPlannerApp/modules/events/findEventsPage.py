from flask import redirect, render_template

from . import bp
from ... import dbInterface

@bp.route("/findevents")
def findEventsPageRoute():
    resultingEvents = dbInterface.fetchAll("select * from events where accessStatus = 'public' ", {})
    data = {
        "events": resultingEvents
    }
    return render_template("events/findEvents.html", data=data)
