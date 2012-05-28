#
# Copyright (c) 2012 Georges Toth <georges _at_ trypill _dot_ org>
#
# This file is part of MeMaTool.
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MeMaTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.

import cgi

from paste.urlparser import PkgResourcesParser
from pylons import request, url
from pylons.controllers.util import forward, redirect
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
    '''
          resp = request.environ.get('pylons.original_response')

    content = ''
    try:
      content = literal(resp.body) or cgi.escape(request.GET.get('message', ''))
    except:
      pass

    c.heading = content

    return render('/unauthorized.mako')
    '''
    request = self._py_object.request
    resp = request.environ.get('pylons.original_response')

    try:
        content = literal(resp.body) or cgi.escape(request.GET.get('message', ''))

        page = error_document_template % \
            dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                 code=cgi.escape(request.GET.get('code', str(resp.status_int))),
                 message=content)
    except:
      # resp can be None !
      # @TODO do log what happened here ... not normal
      redirect(url(controller='profile', action='index'))
      pass

    return page

  def unauthorized(self):
    c.heading = '401'
    return render('/unauthorized.mako')

  def forbidden(self):
    c.heading = '403'
    return render('/unauthorized.mako')

  def _require_auth(self):
    return False
