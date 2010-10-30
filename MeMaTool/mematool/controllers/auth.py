import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render
from pylons.decorators.secure import https


log = logging.getLogger(__name__)

class AuthController(BaseController):

	def index(self,environ):
		if self.identity is not None:
			redirect(url(controller='members', action='showAll'))
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
				redirect(request.params['came_from'])
			else:
				redirect(url(controller='members', action='showAll'))

		return render('/auth/login.mako')
