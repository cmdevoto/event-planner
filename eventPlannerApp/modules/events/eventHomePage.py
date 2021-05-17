from flask import redirect, render_template
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from datetime import date
from . import bp
from ... import dbInterface

@bp.route("/events")
@login_required
def eventHomePageRoute():
    today = date.today()
    formattedToday = today.strftime("%d-%b-%y")
    
    school = dbInterface.fetchOne("select associatedSchool from users where username = (:uname)", {"uname": current_user.get_id()})
    
    resultingEvents = dbInterface.fetchAll("select * from events where eventtime > (:today) and associatedSchool = (:school) and (eventID in (select eventID from eventInvitations where inviteeUsername = (:iid) and status = 'Accepted') or ownerUsername = (:iid) or creatorUsername = (:iid))", {"school": school[0], "iid" : current_user.get_id(), "today" : formattedToday})


    data = {
        "events": resultingEvents
    }
    return render_template("events/eventHome.html", data=data)
