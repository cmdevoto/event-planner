from flask import redirect, render_template

from . import bp
from ... import dbInterface

@bp.route("/createinvitation")
def createInvitationPageRoute():
    resultingUsers = dbInterface.fetchAll("select * from users", {})
    data = {
        "users": resultingUsers
    }
    return render_template("invitations/createInvitation.html", data=data)
