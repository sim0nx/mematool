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
from sqlalchemy import and_
from mematool import Config
from mematool.controllers import BaseController
from mematool.helpers.ldapConnector import LdapConnector
from mematool.model.dbmodel import Preferences
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker, InvalidParameterFormat
from mematool.helpers.crypto import encodeAES
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
      ParamChecker.checkUsername('username', param=True)
      ParamChecker.checkPassword('password', 'password', param=True)
    except InvalidParameterFormat as ipf:
      return self.index(_('Invalid data'))

    try:
      ldap_connector = LdapConnector(username=username, password=password)
    except mematool.helpers.exceptions.InvalidCredentials:
      return self.index(_('Invalid credentials'))
    except mematool.helpers.exceptions.ServerError:
      return self.index(_('Server error, please retry later'))

    old_session_language = self.session.get('language', '')

    self.session.regenerate()
    self.session['username'] = username
    self.session['password'] = encodeAES(password)
    self.set_ldapcon(ldap_connector.get_connection())
    self.session['groups'] = self.mf.getUserGroupList(username)

    try:
      user = self.mf.getUser(self.session['username'])
    except:
      return self.index(_('Server error, please retry later'))

    self.session['user'] = user

    if self.is_admin():
      self.session['pendingMemberValidations'] = self.pendingMemberValidations()

    uidNumber = user.uidNumber
    language = self.db.query(Preferences).filter(and_(Preferences.uidNumber == uidNumber, Preferences.key == 'language')).one()

    if language.value in self.languages:
      self.session['language'] = language.value
    elif not old_session_language == '':
      self.session['language'] = old_session_language
    else:
      self.session['language'] = self.default_language

    log.info(username + ' logged in')

    if user.is_admin():
      raise HTTPRedirect('/members/index')
    else:
      raise HTTPRedirect('/profile/index')

  @cherrypy.expose
  def doLogout(self):
    self.session.clear()
    log.info('{0} logged out'.format(self.session.get('username')))
    return self.index(errorMsg='You logged out')
