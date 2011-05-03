"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako as render
from pylons import session, request, url
import logging

from mematool.model.meta import Session
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter


class BaseController(WSGIController):
    def __init__(self):
	self.authAdapter = LDAPAuthAdapter()
	self.identity = None
	self.log = logging.getLogger(__name__)

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
        #    self.identity = environ.get('repoze.who.identity')

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
	return False
