from flask import render_template

from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField
from wtforms.validators import DataRequired

import calendar

from . import bp
from ... import dbInterface


@bp.route('/event/edit/<int:eventId>')
def event_edit_page(eventId):
    eventQuery = "select * from events where eventId=:eventId"
    eventQueryParams = {
      "eventId": eventId
    }
    eventFromDb = dbInterface.fetchOne(eventQuery, eventQueryParams)

    eventDateTime = eventFromDb[2]
    dateString = "{}, {} {}, {}".format(
      eventDateTime.strftime("%A"),
      calendar.month_name[eventDateTime.month], 
      eventDateTime.day, 
      eventDateTime.year
    )
    timeString = eventDateTime.strftime("%I:%M %p")

    event = {
      "name": eventFromDb[1],
      "time": timeString,
      "date": dateString,
      "location": eventFromDb[3],
      "ownerUsername": eventFromDb[4],
      "ownerName": "",
      "accessType": eventFromDb[5],
      "associatedSchool": eventFromDb[6],
      "creatorUsername": eventFromDb[7],
      "creatorName": ""
    }

    ownerQuery = "select firstname, lastname from users where username = :ownerUsername"
    ownerQueryParams = { "ownerUsername": eventFromDb[4] }
    owner = dbInterface.fetchOne(ownerQuery, ownerQueryParams)
    event["ownerName"] = "{} {}".format(owner[0], owner[1])
    
    if(event["ownerUsername"] != event["creatorUsername"]):
        creatorQuery = "select firstname, lastname from users where username = :creatorUsername"
        creatorQueryParams = { "creatorUsername": eventFromDb[7] }
        creator = dbInterface.fetchOne(creatorQuery, creatorQueryParams)
        event["creatorName"] = "{} {}".format(creator[0], creator[1])
    
    data = {
      "eventId": eventId,
      "event": event
    }

    form = EditEventForm()

    return render_template('events/editEvent.html', form=form, data=data)


class EditEventForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    ownerUsername = StringField('Owner', validators=[DataRequired()])
    accessStatus = SelectField('Visibility', 
        choices=[('private', 'Private'), ('public', 'Public')], 
        validators=[DataRequired()])
    associatedSchool = StringField('Campus', validators=[DataRequired()])
    creatorUsername = StringField('Creator', validators=[DataRequired()])

    
