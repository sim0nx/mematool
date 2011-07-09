"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako as render
from pylons import session, request, url, config
import logging

from mematool.model.meta import Session
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter
from mematool.lib.helpers import *
import re


class BaseController(WSGIController):
	def __init__(self):
		self.authAdapter = LDAPAuthAdapter()
		self.identity = None
		self.log = logging.getLogger(__name__)

		# get the list of admins from the configuration file
		# replace whitespace and split on comma
		self.admins = re.sub(r' ', '', config.get('mematool.admins')).split(',')


	def __call__(self, environ, start_response):
		"""Invoke the Controller"""
		# WSGIController.__call__ dispatches to the Controller method
		# the request is routed to. This routing information is
		# available in environ['pylons.routes_dict']
		try:
		#	self.identity = environ.get('repoze.who.identity')

			return WSGIController.__call__(self, environ, start_response)
		finally:
			Session.remove()



	def __before__(self):
		self.identity = session.get("identity")

		if self.identity:
			request.environ["REMOTE_USER"] = self.identity
		else:
			if self._require_auth():
				referer = request.environ.get('PATH_INFO')
				session["after_login"] = referer
				self.log.debug("setting session['after_login'] to %r", referer)
				session.save()
				redirect(url(controller='auth', action='login'))


	def _require_auth(self):
		return True


	def _isParamSet(self, param):
		if param in request.params and request.params[param] != '':
			return True

		return False


	def _isParamStr(self, param, min_len=0, max_len=255, regex=None):
		if self._isParamSet(param) and len(request.params[param]) > min_len  and len(request.params[param]) <= max_len:
			if regex != None:
				if re.match(regex, request.params[param], re.IGNORECASE):
					return True
			else:
				return True

		return False


	def _isParamInt(self, param, min_val=0, min_len=0, max_len=4):
		if self._isParamStr(param, min_len, max_len) and IsInt(request.params[param]) and int(request.params[param]) > min_val:
			return True

		return False


	def _isParamFloat(self, param, min_val=0, min_len=0, max_len=4):
		if self._isParamStr(param, min_len, max_len) and IsFloat(request.params[param]) and float(request.params[param]) > min_val:
			return True

		return False


	def unauthorized(self):
		redirect(url(controller='error', action='unauthorized'))

	@staticmethod
	def needAdmin(f):
		def new_f(self):
			if 'groups' in session:
				for ag in self.admins:
					if ag in session['groups']:
						print '2 group found'
						return f(self)

			self.unauthorized()

		return new_f


	def isAdmin(f):
		if 'groups' in session:
			for ag in self.admins:
				if ag in session['groups']:
					print '1 group found'
					return True

		return False
