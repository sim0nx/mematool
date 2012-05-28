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

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.i18n.translation import _
from pylons.decorators.secure import https

from mematool.lib.base import BaseController, render
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat
from mematool.lib.syn2cat.crypto import encodeAES, decodeAES


log = logging.getLogger(__name__)


class AuthController(BaseController):
  def __init__(self):
    super(AuthController, self).__init__()

  def index(self, environ):
    if self.identity is not None:
      redirect(url(controller='members', action='showAllMembers'))
    else:
      redirect(url(controller='auth', action='login'))

  @https()
  def login(self):
    if self.identity is not None:
      redirect(url(controller='members', action='showAllMembers'))

    c.heading = 'MeMaTool'

    return render('/auth/login.mako')

  def doLogin(self):
    try:
      ParamChecker.checkUsername('username', param=True)
      ParamChecker.checkPassword('password', 'password', param=True)
    except InvalidParameterFormat as ipf:
      session['flash'] = _('Login failed!')
      session['flash_class'] = 'error'
      session.save()

      redirect(url(controller='auth', action='login'))
 
    authAdapter = LDAPAuthAdapter()
    ret = authAdapter.authenticate(request.params['username'], request.params['password'])

    if ret:
      self._clearSession()

      session['identity'] = request.params['username']
      session['secret'] = encodeAES(request.params['password'])
      lmf = LdapModelFactory()
      session['groups'] = lmf.getUserGroupList(request.params['username'])
      # dummy call to set the variable
      self.isFinanceAdmin()
      session.save()

      log.info(request.params['username'] + ' logged in')

      if 'after_login' in session and not 'forbidden' in session["after_login"]:
        redirect(session["after_login"])
      else:
        if self.isAdmin():
          redirect(url(controller='members', action='index'))
        else:
          redirect(url(controller='profile', action='index'))
    else:
      session['flash'] = _('Login failed!')
      session['flash_class'] = 'error'
      session.save()

    redirect(url(controller='auth', action='login'))

  def _clearSession(self, force=False):
    if self.identity is not None or force:
      session.invalidate()
      session.delete()

  def logout(self):
    self._clearSession(force=True)
    redirect(url(controller='auth', action='login'))

  def _require_auth(self):
    return False
