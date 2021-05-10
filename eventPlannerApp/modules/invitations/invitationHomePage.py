from flask import redirect, render_template
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin

from . import bp
from ... import dbInterface

@bp.route("/invitations")
def invitationHomePageRoute():

    resultingInvites = dbInterface.fetchAll("select * from eventInvitations where inviteeUsername = (:iid) and status = 'Pending'", {"iid" : current_user.get_id()})
 
    data = {
        "invitations": resultingInvites
    }
    return render_template("invitations/invitationHome.html", data=data)
