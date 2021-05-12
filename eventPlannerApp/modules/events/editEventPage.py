
from . import bp
from ... import dbInterface


@bp.route('/event/edit/<int:eventId>')
def event_edit_page(eventId):
  return 'TaDa, Editing: {}'.format(eventId)