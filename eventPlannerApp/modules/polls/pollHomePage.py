from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface

@bp.route("/polls")
@login_required
def pollHomePageRoute():
    resultingPolls = dbInterface.fetchAll("select * from polls where pollID in (select pollID from pollRequest where status = 'Pending' and requestedUsername = (:uname))", {"uname": current_user.get_id()})
 
    data = {
        "polls": resultingPolls
    }

    return render_template("polls/pollsHome.html", data=data)
