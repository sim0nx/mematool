import cgi

from paste.urlparser import PkgResourcesParser
from pylons import request
from pylons.controllers.util import forward
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal

from mematool.lib.base import BaseController, render
from pylons import tmpl_context as c

class ErrorController(BaseController):

    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    def document(self):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')

	content = ''
	try:
		content = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
	except:
		pass

	c.heading = content

	return render('/unauthorized.mako')

    def unauthorized(self):
	c.heading = '401'
	return render('/unauthorized.mako')

    def forbidden(self):
	c.heading = '403'
	return render('/unauthorized.mako')
