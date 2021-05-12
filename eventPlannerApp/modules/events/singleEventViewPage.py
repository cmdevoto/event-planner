from flask import redirect, render_template
from flask_login import login_required

from . import bp
from ... import dbInterface

@login_required
@bp.route("/event/<int:postId>")
def single_event_view_page(postId):
    data = {
      "postId": postId,
      "event": ["CS Party"]
    }
    return render_template("events/singleEventView.html", data=data)