import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController

log = logging.getLogger(__name__)

class AuthController(BaseController):

	def index(self,environ):
		identity = environ.get('repoze.who.identity')
		if identity is not None:
			user = identity.get('user')
			return user
		else:
			redirect(url(controller='auth', action='login'))
	
		#if notAuthenticated:
		#	abort(401, 'You are not authenticated')
		
		#if isForbidden:
		#	abort(403, 'You don\'t have rights to accesss this page')


	def login(self):
		return "At login: here be a form"
		pass

	def logout(self):
		return "At logout"
		pass

	def dologin(self):
		return "At dologin"

