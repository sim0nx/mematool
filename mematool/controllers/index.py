# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Georges Toth <georges _at_ trypill _dot_ org>
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

import cherrypy
from cherrypy._cperror import HTTPRedirect
import logging
from mematool import Config
from mematool.controllers import BaseController
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import InvalidParameterFormat
import mematool.helpers.exceptions

log = logging.getLogger(__name__)


class IndexController(BaseController):
  @cherrypy.expose
  def index(self, errorMsg=None):
    """
    The index page of ce1sus. Mainly only an login page

    :param errorMsg: Error message to be displayed
    :type errorMsg: String

    :returns: generated HTML
    """
    if errorMsg:
      self.session['flash'] = errorMsg
      self.session['flash_class'] = 'error'
      self.session.save()

    return self.render('/auth/login.mako', errorMsg=errorMsg)

  @cherrypy.expose
  def setLang(self, lang):
    if lang in Config.get('mematool', 'languages', []):
      self.session['language'] = lang
      self.session.save()

    if 'user' in self.session:
      raise HTTPRedirect('/profile/index')

    raise HTTPRedirect('/')

  @cherrypy.expose
  def doLogin(self, username=None, password=None):
    try:
      self.authenticate(username, password)
    except InvalidParameterFormat as ipf:
      return self.index(_('Invalid data'))
    except mematool.helpers.exceptions.InvalidCredentials:
      return self.index(_('Invalid credentials'))
    except mematool.helpers.exceptions.ServerError:
      return self.index(_('Server error, please retry later'))

    try:
      self.initialize_session(username, password)
    except Exception as e:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      self.detroy_session()
      return self.index(_('Server error, please retry later'))

    if self.session['user'].is_admin():
      raise HTTPRedirect('/members/index')
    else:
      raise HTTPRedirect('/profile/index')

  @cherrypy.expose
  def doLogout(self):
    self.detroy_session()
    log.info('{0} logged out'.format(self.session.get('username')))
    return self.index(errorMsg='You logged out')
