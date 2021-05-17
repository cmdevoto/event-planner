from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface

@bp.route("/mypolls")
@login_required
def myPollsPageRoute():
    resultingPolls = dbInterface.fetchAll("select * from polls where ownerUsername = (:uname)", {"uname" : current_user.get_id()})
 
    data = {
        "polls": resultingPolls
    }

    return render_template("polls/myPolls.html", data=data)
