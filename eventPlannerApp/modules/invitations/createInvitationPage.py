from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required
import smtplib, ssl
from . import bp
from ... import dbInterface
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@bp.route("/createinvitation")
@login_required
def createInvitationPageRoute():

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
    return render_template("invitations/createInvitation.html", data=data)


@bp.route("/createinvitation", methods=['POST'])
def createInvitationSubmit():

    # Setting up email sending
    port = 587  # For SSL
    smtp_server = "smtp.gmail.com"
    emailUser = "noreply.localhost.app@gmail.com"
    emailPass = "ILoveRamzi123!"
    def sendMessage(messageText, recipients):
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(emailUser, emailPass)
            msg = MIMEMultipart()
            msg['From'] = emailUser
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = "You Have A New Pending localhost Invitation!"
            msg.attach(MIMEText(messageText, 'plain', 'utf-8'))
            server.sendmail(emailUser, recipients, msg.as_string())
            server.quit()
            #server.sendmail(emailUser, recipients, messageText)
    event = request.form['eventSelect']
    #print(event.split(':')[0])
    eventID = int(event.split(':')[0])

    inviterUsername = current_user.get_id()


    ### NEED TO CHECK IF USER CAN INVITE PEOPLE ###
    temp = dbInterface.fetchAll("select * from events where eventID = (:eventID)", {"eventID" : eventID})
    accessType = temp[0][5]
    owner = temp[0][4]
    creator = temp[0][7]


    if (accessType == "Private" or accessType == "private") and (owner != inviterUsername or creator != inviterUsername):
        flash("You do not have permission to invite others to this event.")
        return redirect("/createinvitation")


    # list of people invited
    inviteeUsernames = request.form.getlist('userSelect')

    # list of groups invited
    groups = request.form.getlist('groupSelect')
    groupID = []
    for g in groups:
        groupID.append(int(g.split(':')[0]))
        #groupID.append(int(g[0]))

    message = request.form['message']

    # make list of all people invited , only send one invitation to each person

    if inviteeUsernames:
        inviteSet = set(inviteeUsernames)
    else:
        inviteSet = set()

    for gid in groupID:
        tempQuery = dbInterface.fetchAll("select * from groupMembership where groupID = (:groupID)", {"groupID" : gid})
        for t in tempQuery:
            inviteSet.add(t[0])
        ownerQuery = dbInterface.fetchOne("select ownerUsername from groups where ownerUsername = (:ownerUsername)", {"ownerUsername": owner})
        inviteSet.add(ownerQuery[0])

    if current_user.get_id() != owner:
        inviteSet.add(owner)
    if current_user.get_id() != creator:
        inviteSet.add(creator)

    emailList = []

    # loop to make invitations (insert into eventInvitations)
    for i in inviteSet:

        # check to see if a user has already been invited to the event
        isPresent = dbInterface.fetchOne("select * from eventInvitations where eventID = (:eventID) and inviteeUsername = (:uname)", {"eventID" : eventID, "uname": i})
        if isPresent:
            flash("One of your selected users has already received an invitation. Please fix and try again.")
            return redirect("/createinvitation")

        inviteInsertQuery =  "insert into eventInvitations (eventID, inviterUsername, inviteeUsername, invitationMessage, status) values (:eventID, :inviterUsername, :inviteeUsername, :invitationMessage, :status)"

        inviteInsertParams = {
        "eventID": eventID,
        "inviterUsername": inviterUsername,
        "inviteeUsername": i,
        "invitationMessage": message,
        "status": "Pending"
        }

        result = dbInterface.commit(inviteInsertQuery, inviteInsertParams)

        inviteEmailQuery = "select email from users where username = :username"
        inviteEmailParams = {
            "username": i
        }

        result2 = dbInterface.fetchOne(inviteEmailQuery, inviteEmailParams)
        emailList.append(result2[0])

    #sending an email to the people invited
    formattedMessage = "You have been invited by " + inviterUsername + " to the event: " + event + "\n" + inviterUsername + " said: \n" + message
    if(emailList):
        sendMessage(formattedMessage, emailList)


    return redirect("/invitations")
