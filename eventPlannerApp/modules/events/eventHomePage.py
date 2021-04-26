from flask import redirect, render_template

from . import bp
from ... import dbInterface

@bp.route("/events")
def eventHomePageRoute():
    resultingEvents = dbInterface.fetchAll("select * from events", {})
    data = {
        "events": resultingEvents
    }
    return render_template("events/eventHome.html", data=data)
