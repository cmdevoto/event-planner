from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required
from . import bp
from ... import dbInterface
import sys

@bp.route("/creategroup")
@login_required
def createGroupPageRoute():

    school = dbInterface.fetchOne("select associatedSchool from users where username = (:uname)", {"uname": current_user.get_id()}) 
    print(school)
    print(current_user.get_id())
    params = {
        "school": school[0]
    }

    resultingUsers = dbInterface.fetchAll("select username from users where associatedSchool = (:school)", params)
    print(resultingUsers)
    data = {
        "users": resultingUsers
    }
    print(current_user.get_id())
    return render_template("groups/createGroup.html", data=data)


@bp.route("/creategroup", methods=['POST'])
def createGroupSubmit():
    
    groupName = request.form['groupName']
    groupDesc = request.form['groupDesc']
    ownerUsername = current_user.get_id()
    associatedSchool = dbInterface.fetchOne("select associatedSchool from users where username = (:uname)", {"uname": current_user.get_id()})
    

    groupInsertQuery = "insert into groups (groupName, groupDesc, ownerUsername, associatedSchool) values (:groupName, :groupDesc, :ownerUsername, :associatedSchool)"
    params = {
        "groupName": groupName,
        "groupDesc": groupDesc,
        "ownerUsername": ownerUsername,
        "associatedSchool": associatedSchool[0]
    }

    result = dbInterface.commit(groupInsertQuery, params)

    # SEND GROUP INVITES TO ALL PEOPLE SELECTED

    groupID = dbInterface.fetchOne("select groupID from groups where rownum=1 order by groupID desc", {})

    # list of people invited
    inviteeUsernames = request.form.getlist('userSelect')
    message = request.form['message']
    
    # loop to make invitations (insert into eventInvitations)
    for i in inviteeUsernames:
        membershipInsert =  "insert into groupMembership (username, groupID, status, invitationMessage) values (:username, :groupID, :status, :invitationMessage)"
    
        membershipParams = {
        "username": i,
        "groupID": groupID[0],
        "status": "Pending",
        "invitationMessage": message
        }
    
        result = dbInterface.commit(membershipInsert, membershipParams)

    return redirect("/groups")
