from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface

@bp.route("/viewgroupinvites")
@login_required
def viewGroupInvitationsPageRoute():
    resultingInvites = dbInterface.fetchAll("select * from groupMembership where username = (:iid) and status = 'Pending'", {"iid" : current_user.get_id()})
 
    inviteInfo = []
    for i in resultingInvites:
        groupInfo = dbInterface.fetchOne("select * from groups where groupID = (:id)", {"id" : i[1]})
        inviteInfoDict = {}
        inviteInfoDict = {
            "groupID": i[1],
            "username" : i[0],
            "message" : i[3],
            "status" : i[2],
            "groupName" : groupInfo[1],
            "groupDesc" : groupInfo[2],
            "ownerUsername" : groupInfo[3]
        }
        inviteInfo.append(inviteInfoDict)
    data = {
        "invitationInfo" : inviteInfo
    }

    return render_template("groups/viewGroupInvites.html", data=data)

@bp.route("/viewgroupinvites", methods=['POST'])
def acceptGroupInvitationSubmit():

    try:
        groupID = request.args.get('groupID')
        username = current_user.get_id()
    except:
        flash("An error occured processing your request.")
        return redirect("/viewgroupinvites")


    acceptQuery = "update groupMembership set status = 'Accepted' where groupID = (:groupID) and username = (:username)"    
    queryParams = {
        "groupID": groupID,
        "username": username
    }

    result = dbInterface.commit(acceptQuery, queryParams)
    flash('You successfully accepted this group invitation')
    return redirect("/viewgroupinvites")
