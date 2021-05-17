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
    print(resultingEvents)
    resultingUsers = dbInterface.fetchAll("select username from users where associatedSchool = (:school)", params)
    resultingGroups = dbInterface.fetchAll("select groupID, groupName from groups where associatedSchool = (:school)", params)
    data = {
        "events": resultingEvents,
        "users": resultingUsers,
        "groups": resultingGroups
    }
    print(current_user.get_id())
    return render_template("invitations/createInvitation.html", data=data)


@bp.route("/createinvitation", methods=['POST'])
def createInvitationSubmit():
    
    # Setting up email sending
    port = 587  # For SSL
    smtp_server = "smtp.gmail.com"
    emailUser = "noreply.localhost.app@gmail.com"
    emailPass = "ILoveRamzi123!"
    def sendMessage(messageText, recipients):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.starttls()
            server.login(emailUser, emailPass)
            msg = MIMEMultipart()
            msg['From'] = emailUser
            msg['To'] = recipients
            msg['Subject'] = "localhost Invitation"
            print(messageText)
            msg.attach(MIMEText(messageText, 'text'))
            s.send_message(msg)
            s.quit()
            #server.sendmail(emailUser, recipients, messageText)
    print("email set up")
    event = request.form['eventSelect']
    #print(event.split(':')[0])
    eventID = int(event.split(':')[0])

    inviterUsername = current_user.get_id()


    ### NEED TO CHECK IF USER CAN INVITE PEOPLE ###
    print("CREATE INVITE . PY")
    temp = dbInterface.fetchAll("select * from events where eventID = (:eventID)", {"eventID" : eventID})
    print(temp)
    accessType = temp[0][5]
    owner = temp[0][4]
    creator = temp[0][7]

    print(accessType)
    print(owner)
    print(creator)

    if accessType == "Private" or accessType == "private" and (owner != inviterUsername or creator != inviterUsername):
        print("you don't have permissions to invite others to this event")    
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

    print(event, file=sys.stderr)
    print(eventID, file=sys.stderr)
    print(inviterUsername, file=sys.stderr)
    print(inviteeUsernames, file=sys.stderr)
    print(groups, file=sys.stderr)
    print(groupID, file=sys.stderr)
    print(message, file=sys.stderr)

    # make list of all people invited , only send one invitation to each person

    if inviteeUsernames:
        inviteSet = set(inviteeUsernames)
    else:
        inviteSet = set()   
    
    for gid in groupID:
        tempQuery = dbInterface.fetchAll("select * from groupMembership where groupID = (:groupID)", {"groupID" : gid})
        print(tempQuery)
        for t in tempQuery:
            inviteSet.add(t[0])
    print(inviteSet)

    emailList = []

    # loop to make invitations (insert into eventInvitations)
    for i in inviteSet:
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
    formattedMessage = "You have been invited by " + inviterUsername + " to the event: \n" + event + "\nThey said: \n" + message
    print(formattedMessage)
    sendMessage(formattedMessage, emailList)


    return redirect("/invitations")
