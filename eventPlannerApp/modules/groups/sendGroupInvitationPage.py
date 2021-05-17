from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required
from . import bp
from ... import dbInterface
import sys

@bp.route("/sendgroupinvite")
@login_required
def sendGroupInvitationPageRoute():

    school = dbInterface.fetchOne("select associatedSchool from users where username = (:uname)", {"uname": current_user.get_id()}) 
    params = {
        "school": school[0]
    }
    
    resultingUsers = dbInterface.fetchAll("select username from users where associatedSchool = (:school)", params)
    resultingGroups = dbInterface.fetchAll("select groupID, groupName from groups where associatedSchool = (:school)", params)
    data = {
        "users": resultingUsers,
        "groups": resultingGroups
    }
    print(data["groups"])

    print(current_user.get_id())
    return render_template("groups/sendGroupInvite.html", data=data)


@bp.route("/sendgroupinvite", methods=['POST'])
def sendGroupInvitationSubmit():
    
    
    # list of people invited
    inviteeUsernames = request.form.getlist('userSelect')
    
    group = request.form['groupSelect']
    groupID = int(group.split(':')[0])

    ownerUsername = dbInterface.fetchOne("select ownerUsername from groups where groupID = (:groupID)", {"groupID": groupID})
    
    if ownerUsername[0] != current_user.get_id():
        flash("You do not have permission to invite others to join this group.")
        return redirect("/creategroupinvite")

    message = request.form['message']

    # insert into groupMembership
    # i think we should check to see if something exists currently
    
    for i in inviteeUsernames:
        
        isPresent = dbInterface.fetchOne("select * from groupMembership where username = (:username) and groupID = (:groupID)", {"username": i, "groupID": groupID})
        if isPresent:
            flash("One of your selected users already belongs to the group. Please fix and try again.")
            return redirect("/sendgroupinvite")
        
        inviteInsertQuery = "insert into groupMembership values (:username, :groupID, :status, :invitationMessage)"
    
        inviteInsertParams = {
        "username": current_user.get_id(),
        "groupID": groupID,
        "status": "Pending",
        "invitationMessage": message
        }
    
        result = dbInterface.commit(inviteInsertQuery, inviteInsertParams)

    return redirect("/groups")
