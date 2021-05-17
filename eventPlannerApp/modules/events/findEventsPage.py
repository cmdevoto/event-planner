from flask import redirect, render_template
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from datetime import date
from . import bp
from ... import dbInterface

@bp.route("/findevents")
@login_required
def findEventsPageRoute():
    today = date.today()
    formattedToday = today.strftime("%d-%b-%y")
    resultingEvents = dbInterface.fetchAll("select * from events where eventtime > (:today) and accessStatus = (:status)", {"status": "Public", "today" : formattedToday})
    data = {
        "events": resultingEvents
    }
    return render_template("events/findEvents.html", data=data)
