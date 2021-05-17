from flask import redirect, render_template
from flask_login import current_user, login_user, LoginManager, login_required, logout_user

from . import bp
from ... import dbInterface

@bp.route("/events")
@login_required
def eventHomePageRoute():

    #resultingEvents = dbInterface.fetchAll("select * from events", {})
    resultingEvents = dbInterface.fetchAll("select * from events where eventID in (select eventID from eventInvitations where inviteeUsername = (:iid) and status = 'Accepted') or ownerUsername = (:iid) or creatorUsername = (:iid)", {"iid" : current_user.get_id()})


    data = {
        "events": resultingEvents
    }
    return render_template("events/eventHome.html", data=data)
