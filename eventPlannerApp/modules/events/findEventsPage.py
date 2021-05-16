from flask import redirect, render_template
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

from . import bp
from ... import dbInterface

@bp.route("/findevents")
@login_required
def findEventsPageRoute():
    resultingEvents = dbInterface.fetchAll("select * from events where accessStatus = (:status)", {"status": "Public"})
    data = {
        "events": resultingEvents
    }
    return render_template("events/findEvents.html", data=data)
