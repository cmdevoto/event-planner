from flask import render_template

from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, SelectField
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
      "hour": eventDateTime.hour,
      "minute": eventDateTime.minute,
      "amPm": eventDateTime.strftime("%p"),
      "day": eventDateTime.day,
      "month": eventDateTime.month,
      "year": eventDateTime.year,
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
    day = IntegerField('Day', validators=[DataRequired()])
    month = SelectField('Month',
        choices=[],
        validators=[DataRequired()]
        )
    year = IntegerField('Year', validators=[DataRequired()])
    hour = IntegerField('Hour', validators=[DataRequired()])
    minute = IntegerField('Minute', validators=[DataRequired()])
    amPm = SelectField('AM/PM', 
        choices=[('AM', 'AM'), ('PM', 'PM')],
        validotrs=[DataRequired()]
        )
    date = DateField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    ownerUsername = StringField('Owner', validators=[DataRequired()])
    accessStatus = SelectField('Visibility', 
        choices=[('private', 'Private'), ('public', 'Public')], 
        validators=[DataRequired()]
        )
    associatedSchool = StringField('Campus', validators=[DataRequired()])
    creatorUsername = StringField('Creator', validators=[DataRequired()])

    
