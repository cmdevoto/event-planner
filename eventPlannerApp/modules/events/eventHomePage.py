from flask import redirect, render_template
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin

from . import bp
from ... import dbInterface

@bp.route("/events")
def eventHomePageRoute():

    #resultingEvents = dbInterface.fetchAll("select * from events", {})
    resultingEvents = dbInterface.fetchAll("select * from events where eventID in (select eventID from eventInvitations where inviteeUsername = (:iid) and status = 'Accepted') or ownerUsername = (:iid) or creatorUsername = (:iid)", {"iid" : current_user.get_id()})


    data = {
        "events": resultingEvents
    }
    return render_template("events/eventHome.html", data=data)
