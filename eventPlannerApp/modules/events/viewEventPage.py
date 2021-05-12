from flask import redirect, render_template

from . import bp
from ... import dbInterface


@bp.route("/event/<int:postId>")
def single_event_view_page():
  return ''