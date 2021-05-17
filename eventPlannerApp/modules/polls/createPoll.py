from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required

from . import bp
from ... import dbInterface
import sys

@bp.route("/createpoll")
@login_required
def createPollPageRoute():

    school = dbInterface.fetchOne("select associatedSchool from users where username = (:uname)", {"uname": current_user.get_id()}) 
    params = {
        "school": school[0]
    }

    resultingEvents = dbInterface.fetchAll("select eventID, description from events where associatedSchool = (:school)", params)
    resultingUsers = dbInterface.fetchAll("select username from users where associatedSchool = (:school)", params)
    resultingGroups = dbInterface.fetchAll("select groupID, groupName from groups where associatedSchool = (:school)", params)
    data = {
        "events": resultingEvents,
        "users": resultingUsers,
        "groups": resultingGroups
    }
    print(current_user.get_id())
    return render_template("polls/createPoll.html", data=data)


@bp.route("/createpoll", methods=['POST'])
def createPollSubmit():
    
    event = request.form['eventSelect']
    #print(event.split(':')[0])
    eventID = int(event.split(':')[0])

    ownerUsername = current_user.get_id()

    pollInsert = "insert into polls (eventID, ownerUsername, title, description) values (:eventID, :ownerUsername, :title, :description)"
    insertParams = {
        "eventID" : eventID,
        "ownerUsername": ownerUsername,
        "title": request.form['title'],
        "description": request.form['description']
    }

    insertResult = dbInterface.commit(pollInsert, insertParams)

    ## sending poll requests to those selected

    inviteeUsernames = request.form.getlist('userSelect')

    # list of groups invited
    groups = request.form.getlist('groupSelect')
    groupID = []
    for g in groups:
        groupID.append(int(g.split(':')[0]))

    # make list of all people invited , only send one invitation to each person

    if inviteeUsernames:
        inviteSet = set(inviteeUsernames)
    else:
        inviteSet = set()

    for gid in groupID:
        tempQuery = dbInterface.fetchAll("select * from groupMembership where groupID = (:groupID)", {"groupID" : gid})
        for t in tempQuery:
            inviteSet.add(t[0])
    print(inviteSet)
    print("HERE")

    # get poll ID
    pollID = dbInterface.fetchOne("select pollID from polls where rownum = 1 order by pollID desc", {})

    print(pollID)

    for i in inviteSet:
        print(i)
        requestQuery = "insert into pollRequest (pollID, requestedUsername, status) values (:pollID, :requestedUsername, :status)"

        params = {
        "pollID": pollID[0],
        "requestedUsername": i,
        "status": "Pending"
        }

        result = dbInterface.commit(requestQuery, params)

    return redirect("/polls")
