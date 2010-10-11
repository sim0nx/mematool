import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member

log = logging.getLogger(__name__)

from mematool.lib.syn2cat.ldapConnector import LdapConnector


class MembersController(BaseController):

	def __init__(self):
		self.ldapcon = LdapConnector()


	def index(self):
		return self.showMember()

		members_q = Session.query(Member)
		members = members_q.all()
		c.members = members

		return render('/members/index.mako')


	def showMember(self):
		member_q = Session.query(Member).filter(Member.idmember == 1)
		member = member_q.one()
	
		member.mobile = "2"
		member.dtusername = 'sim0n'
		if not member.loadFromLdap():
			print "uh, member does not exist!"

		c.member = member

		return render('/members/view.mako')
