import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render

log = logging.getLogger(__name__)

class MembersController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/members.mako')
        # or, return a string
        return 'Hello World'
