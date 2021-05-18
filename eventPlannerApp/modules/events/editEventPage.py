from flask import render_template, redirect
from flask.helpers import url_for

from flask_login import login_required

from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired, NumberRange

import calendar
from datetime import datetime

from . import bp
from ... import dbInterface

@login_required
@bp.route('/event/edit/<int:eventId>', methods=['GET', 'POST'])
def editEventPageRoute(eventId):
    eventQuery = "select * from events where eventId=:eventId"
    eventQueryParams = {
      "eventId": eventId
    }
    eventFromDb = dbInterface.fetchOne(eventQuery, eventQueryParams)

     if not eventFromDb:
        print("no event from db")
        return redirect("/events")

    eventDateTime = eventFromDb[2]
    event = {
      "eventId": eventFromDb[0],
      "name": eventFromDb[1],
      "hour": eventDateTime.strftime("%-I"),
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

    print("Trying to edit: {} {}".format(event["ownerUsername"], current_user.get_id()))

    if current_user.get_id() != event["ownerUsername"]:
        return redirect("/events")

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

    if form.validate_on_submit():
        #print('Form Submitted: {}'.format(form))

        updateEventQuery = '''update events
          set description = :description, eventTime = :eventTime, location = :location,
              accessStatus = :accessStatus, associatedSchool = :associatedSchool
          where eventId = :eventId
          '''

        #print("Hour: {}".format(form.hour.data))
        #print("AMPM: {}".format(form.amPm.data))

        updateEventQueryArgs = {
          'description': form.description.data,
          'eventTime': datetime(
            year=int(form.year.data),
            month=int(form.month.data),
            day=int(form.day.data),
            hour=int(form.hour.data) if form.amPm == 'PM' else int(form.hour.data) + 12,
            minute=int(form.minute.data),
            ),
          'location': form.location.data,
          'accessStatus': form.accessType.data,
          'associatedSchool': form.associatedSchool.data,
          'eventId': eventId
        }
        dbInterface.commit(updateEventQuery, updateEventQueryArgs)
        return redirect(url_for('.viewEventPageRoute', eventId=eventId))

    form.description.data = event['name']
    form.day.data = event['day']
    form.month.data = '{}'.format(event['month'])
    form.year.data = event['year']
    form.hour.data = event['hour']
    form.minute.data = event['minute']
    form.amPm.data = event['amPm']
    form.location.data = event['location']
    form.ownerUsername.data = event['ownerUsername']
    form.accessType.data = event['accessType']
    form.associatedSchool.data = event['associatedSchool']
    form.creatorUsername.data = event['creatorUsername']

    return render_template('events/editEvent.html', form=form, data=data)


class EditEventForm(FlaskForm):
    description = StringField('Name', validators=[DataRequired(message="Name is a required field.")])
    day = IntegerField('Day', validators=[DataRequired(message="Day is a required field."), NumberRange(message="Day should be between 1 and 31.", min=1, max=31)])
    month = SelectField('Month',
        choices=[ ( '1', calendar.month_name[1]),  ( '2', calendar.month_name[2]),  ( '3', calendar.month_name[3]),
                  ( '4', calendar.month_name[4]),  ( '5', calendar.month_name[5]),  ( '6', calendar.month_name[6]),
                  ( '7', calendar.month_name[7]),  ( '8', calendar.month_name[8]),  ( '9', calendar.month_name[9]),
                  ('10', calendar.month_name[10]), ('11', calendar.month_name[11]), ('12', calendar.month_name[12])],
        validators=[DataRequired(message="Month is a required field.")]
        )
    year = IntegerField('Year', validators=[DataRequired(message="Year is a required field."), NumberRange(message="Year should be a valid year number.", min=1900, max=2400)])
    hour = IntegerField('Hour', validators=[DataRequired(message="Hour is a required field."), NumberRange(message="Hour should be between 1 and 12.", min=1, max=12)])
    minute = IntegerField('Minute', validators=[DataRequired(message="Minute is a required field."), NumberRange(message="Minute should be between 1 and 60.", min=1, max=60)])
    amPm = SelectField('AM/PM',
        choices=[('AM', 'AM'), ('PM', 'PM')],
        validators=[DataRequired()]
        )
    location = StringField('Location', validators=[DataRequired(message="Location is a required field.")])
    ownerUsername = StringField('Owner', validators=[DataRequired(message="Owner is a required field.")])
    accessType = SelectField('Visibility',
        choices=[('public', 'Public'), ('private', 'Private')],
        validators=[DataRequired(message="Visibility is a required field.")]
        )
    associatedSchool = StringField('Campus', validators=[DataRequired(message="Campus is a required field.")])
    creatorUsername = StringField('Creator', validators=[DataRequired(message="Creator is a required field.")])
