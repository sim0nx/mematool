import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render
from pylons.decorators.secure import https
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.lib.syn2cat.crypto import encodeAES, decodeAES


log = logging.getLogger(__name__)

class AuthController(BaseController):
	def __init__(self):
		super(AuthController, self).__init__()

	def index(self,environ):
		if self.identity is not None:
			redirect(url(controller='members', action='showAllMembers'))
		else:
			redirect(url(controller='auth', action='login'))
	
		#if notAuthenticated:
		#	abort(401, 'You are not authenticated')
		
		#if isForbidden:
		#	abort(403, 'You don\'t have rights to accesss this page')


	@https()
	def login(self):
		if self.identity is not None:
			if 'came_from' in request.params:
				#redirect(request.params['came_from'])
				redirect(url(controller='members', action='showAllMembers'))
			else:
				redirect(url(controller='members', action='showAllMembers'))

		c.heading = 'MeMaTool'

		return render('/auth/login.mako')


	def doLogin(self):
		if not 'username' in request.params or request.params['username'] == '' or not 'password' in request.params or request.params['password'] == '':
			print "crap"
		else:
			authAdapter = LDAPAuthAdapter()
			ret = authAdapter.authenticate(request.params['username'], request.params['password'])

			if ret:
				self._clearSession()
				lmf = LdapModelFactory()

				session['identity'] = request.params['username']
				session['secret'] = encodeAES( request.params['password'] )
				session['groups'] = lmf.getUserGroupList(request.params['username'])
				session.save()

				if 'after_login' in session and not 'forbidden' in session["after_login"]:
					print session["after_login"]
					redirect(session["after_login"])
				else:
					if self.isAdmin():
						redirect(url(controller='members', action='index'))
					else:
						redirect(url(controller='profile', action='index'))

		redirect(url(controller='auth', action='login'))


	def _clearSession(self):
		if self.identity is not None:
			session['identity'] = None
			session.invalidate()
			session.save()
			session.delete()
			request.environ["REMOTE_USER"] = ''


	def logout(self):
		self._clearSession()

		redirect(url(controller='auth', action='login'))

	def _require_auth(self):
		return False
