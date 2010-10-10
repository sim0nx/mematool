import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member

log = logging.getLogger(__name__)

class MembersController(BaseController):

	def index(self):
		members_q = Session.query(Member)
		c.members = members_q.all()

		return render('/members/index.mako')
