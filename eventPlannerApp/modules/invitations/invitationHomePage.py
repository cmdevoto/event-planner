from flask import redirect, render_template

from . import bp
from ... import dbInterface

@bp.route("/invitations")
def invitationHomePageRoute():
    # will have to something along the lines of:
    # select * from invitations where user_id = <user> and status = "Pending"

    resultingInvitations = dbInterface.fetchAll("select * from eventInvitations", {})
    data = {
        "invitations": resultingInvitations
    }
    return render_template("invitations/invitationHome.html", data=data)
