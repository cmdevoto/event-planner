from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

import calendar

from . import bp
from ... import dbInterface

@login_required
@bp.route("/groups/admin/<int:groupId>")
def viewGroupPageRoute(groupId):
    
    groupQuery = "select * from groups where groupID = (:groupID)"
    params = {
      "groupID": groupId
    }
    groupFromDB = dbInterface.fetchOne(groupQuery, params)

    # check that user is the owner of the event

    if groupFromDB[3] != current_user.get_id():
        flash("You are not permitted to access this screen")
        return redirect("/groups")

    membersFromDB = dbInterface.fetchAll("select username, status from groupMembership where groupID = (:groupID)", {"groupID": groupId})

    members = []
    for m in membersFromDB:
        userInfo = dbInterface.fetchOne("select firstname, lastname from users where username = (:uname)", {"uname" : m[0]})
        userInfoDict = {
            "username" : m[0],
            "firstName" : userInfo[0],
            "lastName" : userInfo[1],
            "status" : m[1],
            "groupID" : groupId
        }
        members.append(userInfoDict)

    # sort alphabetically by last name
    newMembers = sorted(members, key = lambda i: i['lastName'])

    data = {
        "members" : newMembers,
        "groupInfo" : groupFromDB
    }

    return render_template("groups/viewGroupAdmin.html", data=data)


@bp.route("/groups/admin/<int:groupId>", methods=['POST'])
def deleteMemberPageRoute(groupId):

    try:
        groupID = request.args.get('groupID')
        username = request.args.get('username')
    except:
        flash("An error occured.")
        return redirect("/groups")

    deleteQuery = "delete from groupMembership where groupID = (:groupID) and username = (:username)"
    params = {
        "groupID": groupID,
        "username" : username
    }
    result = dbInterface.commit(deleteQuery, params)
    flash("You successfully removed the user from the group")
    urlString = "/groups/admin/{}".format(groupID)
    return redirect(urlString)


