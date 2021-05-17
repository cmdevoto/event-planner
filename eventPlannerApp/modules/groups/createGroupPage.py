from flask import render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager, UserMixin, login_required
from . import bp
from ... import dbInterface
import sys
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
            print(messageText)
            msg.attach(MIMEText(messageText, 'plain', 'utf-8'))
            server.sendmail(emailUser, recipients, msg.as_string())
            server.quit()

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
    emailList = []
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

        inviteEmailQuery = "select email from users where username = :username"
        inviteEmailParams = {
            "username": i
        }

        result2 = dbInterface.fetchOne(inviteEmailQuery, inviteEmailParams)
        emailList.append(result2[0])

    formattedMessage = "You have been invited by " + ownerUsername + " to the group: \n" + groupName + "\n" + ownerUsername + " said: \n" + message
    print(formattedMessage)
    sendMessage(formattedMessage, emailList)

    return redirect("/groups")
