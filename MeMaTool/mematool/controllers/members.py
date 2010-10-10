import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member

log = logging.getLogger(__name__)

import ldap
from pylons import config

class MembersController(BaseController):

	def __init__(self):
		self.con = ldap.initialize(config.get('ldap.server'))
		try:
		        self.con.start_tls_s()
		        try:
		                self.con.simple_bind_s(config.get('ldap.bind'), config.get('ldap.password'))
		        except ldap.INVALID_CREDENTIALS:
		                print "Your username or password is incorrect."
		except ldap.LDAPError, e:
		        print e.message['info']
		        if type(e.message) == dict and e.message.has_key('desc'):
		                print e.message['desc']
		        else:
		                print e

		        sys.exit()


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
		self.getMember(member)

		c.member = member

		return render('/members/view.mako')


	def getMember(self, member):
		uid = member.dtusername
		uid = "sim0n"
	        filter = '(uid=' + uid + ')'
	        attrs = ['*']

	        result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

	        for dn, attr in result:
	                for key, value in attr.iteritems():
				if key == "mobile":
					member.mobile = value[0]




	def getUserList(self):
	        filter = '(uid=*)'
	        attrs = ['uid', 'uidNumber']

	        result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

	        users = []

	        for dn, attr in result:
	                if int(attr['uidNumber'][0]) >= 1000 and int(attr['uidNumber'][0]) < 65000:
	                        users.append( attr['uid'][0] )

	        return users
