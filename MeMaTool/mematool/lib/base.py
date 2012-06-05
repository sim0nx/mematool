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

'''The base Controller API
Provides the BaseController class for subclassing.
'''
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako as render
from pylons import session, request, url, config
from pylons.i18n.translation import set_lang
import logging

from mematool.model.meta import Session
from mematool.model import TmpMember
from mematool.lib.helpers import *
import re

import smtplib
from email.mime.text import MIMEText


class BaseController(WSGIController):
  def __init__(self):
    self.identity = None
    self.log = logging.getLogger(__name__)

    # seems to be necessary, else the connection is kept around giving unwanted results
    if 'ldapcon' in config['mematool']:
      del(config['mematool']['ldapcon'])

    # get the list of admins from the configuration file
    # replace whitespace and split on comma
    self.admins = re.sub(r' ', '', config.get('mematool.admins')).split(',')
    self.superadmins = re.sub(r' ', '', config.get('mematool.superadmins')).split(',')
    self.financeadmins = re.sub(r' ', '', config.get('mematool.financeadmins')).split(',')
    self.default_language = config.get('mematool.default_language')
    self.languages = re.sub(r' ', '', config.get('mematool.languages')).split(',')

    if self.isAdmin():
      session['pendingMemberValidations'] = self.pendingMemberValidations()
      session.save()

  def __call__(self, environ, start_response):
    """Invoke the Controller"""
    # WSGIController.__call__ dispatches to the Controller method
    # the request is routed to. This routing information is
    # available in environ['pylons.routes_dict']
    if 'language' in session and session['language'] in self.languages:
      set_lang(session['language'])
    else:
      set_lang(self.default_language)

    try:
      return WSGIController.__call__(self, environ, start_response)
    finally:
      Session.remove()

  def __before__(self):
    self.identity = session.get("identity")

    if self.identity:
      request.environ["REMOTE_USER"] = self.identity

      # blind call ... we don't care about the return value
      # but only that the call sets a session variable
      # @TODO silly hack... rework
      self.isFinanceAdmin()
      self.isAdmin()
    else:
      if self._require_auth():
        referer = request.environ.get('PATH_INFO')
        session["after_login"] = referer
        self.log.debug("setting session['after_login'] to %r", referer)
        session.save()
        redirect(url(controller='auth', action='login'))

  def _require_auth(self):
    return True

  def _forbidden(self):
    if not self.identity and not 'identity' in session:
      redirect(url(controller='auth', action='login'))
    else:
      redirect(url(controller='error', action='forbidden'))

  @staticmethod
  def needSuperAdmin(f):
    def new_f(self):
      if self.isSuperAdmin():
        return f(self)

      self._forbidden()

    return new_f

  @staticmethod
  def needAdmin(f):
    def new_f(self):
      if self.isAdmin():
        return f(self)

      self._forbidden()

    return new_f

  @staticmethod
  def needGroup(group):
    def wrap_f(f):
      def new_f(self, *args):
        if self.isInGroup(group):
          return f(self, *args)

        self._forbidden()

      return new_f
    return wrap_f

  @staticmethod
  def needVGroup(group):
    def wrap_f(f):
      def new_f(self, *args):
        if self.isInVGroup(group):
          return f(self, *args)

        self._forbidden()

      return new_f
    return wrap_f

  def isInGroup(self, group):
    if not 'identity' in session or str(group) == '':
      return False

    session_string = 'isInGroup' + str(group)

    if not session_string in session:
      session[session_string] = False

      if 'groups' in session:
        if hasattr(self, group):
          for ag in getattr(self, group):
            if ag in session['groups']:
              session[session_string] = True
              break

      session.save()

    return session[session_string]

  def isInVGroup(self, group):
    if not 'identity' in session or str(group) == '':
      return False

    session_string = 'isInVGroup' + str(group)

    if not session_string in session:
      session[session_string] = False

      if hasattr(self, group):
        if session['identity'] in getattr(self, group):
          session[session_string] = True

      session.save()

    return session[session_string]

  def isAdmin(self):
    session['isAdmin'] = self.isInGroup('admins')
    session.save()
    return session['isAdmin']

  def isFinanceAdmin(self):
    session['isFinanceAdmin'] = self.isInVGroup('financeadmins')
    session.save()
    return session['isFinanceAdmin']

  @staticmethod
  def needFinanceAdmin(f):
    def new_f(self):
      if session['identity'] in self.financeadmins:
        return f(self)

      self._forbidden()

    return new_f

  '''
  @param m Member object
  @param p parameter string
  '''
  def prepareVolatileParameter(self, m, p):
    '''check if a parameter has been removed or changed'''
    if p in request.params:
      if request.params[p] == '' and p in vars(m):
        setattr(m, p, 'removed')
      else:
        setattr(m, p, request.params[p])
    elif p in vars(m) and request.params['mode'] == 'edit':
      setattr(m, p, 'removed')

  def pendingMemberValidations(self):
    count = Session.query(TmpMember).count()

    if count:
      return count

    return 0

  def sendMail(self, to_, subject, body, from_=''):
    msg = MIMEText(body)

    if from_ == '':
      from_ = config.get('mematool.mail_default_from')

    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to_

    s = smtplib.SMTP('localhost')
    s.sendmail(from_, [to_], msg.as_string())
    s.quit()
