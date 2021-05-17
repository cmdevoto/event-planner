from flask import redirect, render_template
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from datetime import date
from . import bp
from ... import dbInterface

@bp.route("/viewPastEvents")
@login_required
def viewPastEvents():
    today = date.today()
    formattedToday = today.strftime("%d-%b-%y")
    #resultingEvents = dbInterface.fetchAll("select * from events", {})
    resultingEvents = dbInterface.fetchAll("select * from events where eventtime < (:today) and (eventID in (select eventID from eventInvitations where inviteeUsername = (:iid) and status = 'Accepted') or ownerUsername = (:iid) or creatorUsername = (:iid))", {"iid" : current_user.get_id(), "today" : formattedToday})


    data = {
        "events": resultingEvents
    }
    return render_template("events/viewPastEvents.html", data=data)
