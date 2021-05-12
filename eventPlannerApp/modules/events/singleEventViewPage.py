from flask import redirect, render_template
from flask_login import login_required

from . import bp
from ... import dbInterface

@login_required
@bp.route("/event/<int:eventId>")
def single_event_view_page(eventId):
    event = dbInterface.fetchOne("select * from events", {})
    print("Event Page: {}".format(event))
    data = {
      "eventId": eventId,
      "event": event
    }
    return render_template("events/singleEventView.html", data=data)