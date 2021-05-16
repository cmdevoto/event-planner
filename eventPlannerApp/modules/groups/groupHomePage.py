from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface

@bp.route("/groups")
@login_required
def groupHomePageRoute():
    resultingGroups = dbInterface.fetchAll("select * from groups where groupID in (select groupID from groupMembership where username = (:uname) and status = 'Accepted')", {"uname" : current_user.get_id()})
 
    data = {
        "groups": resultingGroups
    }

    return render_template("groups/groupHome.html", data=data)

@bp.route("/groups", methods=['POST'])
def leaveGroupSubmit():
    print("leaving group")

    try:
        groupID = request.args.get('groupID')
        username = current_user.get_id()
    except:
        flash("An error occured processing your request.")
        return redirect("/groups")

    leaveQuery = "delete from groupMembership where groupID = (:groupID) and username = (:uname)"
    queryParams = {
        "groupID": groupID,
        "uname": username
    }

    result = dbInterface.commit(leaveQuery, queryParams)
    flash('You successfully left this group')
    return redirect("/groups")
