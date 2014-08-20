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
from cherrypy._cperror import HTTPRedirect, HTTPError
import logging
from mako.lookup import TemplateLookup
import smtplib
from email.mime.text import MIMEText
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from mematool import Config
from mematool.model.dbmodel import TmpMember, Preferences
from mematool.helpers.crypto import decodeAES
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker
from mematool.helpers.crypto import encodeAES

log = logging.getLogger(__name__)


class TemplateContext(object):
  def __init__(self):
    self.heading = ''


class BaseController(object):
  def __init__(self):
    templateRoot = Config.get('mako', 'templateroot')
    collectionSize = Config.get('mako', 'collectionsize')
    outputEncoding = Config.get('mako', 'outputencoding')
    self._mylookup = TemplateLookup(directories=[templateRoot],
                              module_directory=Config.basePath + '/tmp',
                              output_encoding=outputEncoding,
                              encoding_errors='replace',
                              imports=['from mematool.helpers.i18ntool import ugettext as _'])

    self.sidebar = []
    self.languages = Config.get('mematool', 'languages', [])
    self.default_language = Config.get('mematool', 'default_language', 'en')
    self._debug = Config.get_boolean('mematool', 'debug', False)

  def _sidebar(self):
    pass

  def render(self, template_name, template_context=None, **kwargs):
    template = self._mylookup.get_template(template_name)

    if template_context is None:
      c = TemplateContext()
    else:
      c = template_context

    c.pendingMemberValidations = self.pendingMemberValidations()
    c.is_admin = self.is_admin()

    self._sidebar()

    return template.render(session=cherrypy.session, c=c, sidebar=self.sidebar, **kwargs)

  @property
  def debug(self):
    return self._debug

  @property
  def session(self):
    return cherrypy.session

  def initialize_session(self, username, password):
    '''call this method after successful login'''
    old_session_language = self.session.get('language', '')

    self.session.regenerate()
    self.session['username'] = username
    self.session['password'] = encodeAES(password)
    self.session['groups'] = self.mf.getUserGroupList(username)

    user = self.mf.getUser(self.session['username'])

    self.session['user'] = user

    if self.is_admin():
      self.session['pendingMemberValidations'] = self.pendingMemberValidations()

    try:
      language = self.db.query(Preferences).filter(and_(Preferences.uidNumber == user.uidNumber, Preferences.key == 'language')).one()
    except NoResultFound:
      language = None

    if language and language.value in self.languages:
      self.session['language'] = language.value
    elif not old_session_language == '':
      self.session['language'] = old_session_language
    else:
      self.session['language'] = self.default_language

    log.info(username + ' logged in')

  def detroy_session(self):
    self.session.clear()
    self.session.regenerate()

  @property
  def db(self):
    return cherrypy.request.db

  @property
  def request(self):
    return cherrypy.request

  def authenticate(self, username, password):
    ParamChecker.checkUsername('username', param=True)
    ParamChecker.checkPassword('password', 'password', param=True)

    self.mf.authenticate(username, password)

  @property
  def mf(self):
    module_ = 'mematool.model.{0}ModelFactory'.format(Config.get('mematool', 'model_handler'))
    class_ = '{0}ModelFactory'.format(Config.get('mematool', 'model_handler').title())

    t_mod = __import__(module_, fromlist=[module_])
    t_class = getattr(t_mod, class_)

    return t_class()

  def is_in_group(self, group):
    if not group == '' and 'user' in self.session and self.session.get('user').is_in_group(group):
      return True

    return False

  def is_in_vgroup(self, group):
    if not group == '' and 'user' in self.session:
      for vgroup in Config.get('mematool', 'vgroup_{0}'.format(group), []):
        if vgroup in self.session.get('user').groups:
          return True

    return False

  @staticmethod
  def needAdmin(f):
    def new_f(self, *args, **kwargs):
      if 'user' in self.session and self.session['user'].is_admin():
        return f(self, *args, **kwargs)

      raise HTTPError(403, _('You are not allowed to view this ressource'))

    return new_f

  @staticmethod
  def needFinanceAdmin(f):
    def new_f(self, *args, **kwargs):
      if 'user' in self.session and self.session['user'].is_finance_admin():
        return f(self, *args, **kwargs)

      raise HTTPError(403, _('You are not allowed to view this ressource'))

    return new_f

  @staticmethod
  def needGroup(group):
    def wrap_f(f):
      def new_f(self, *args, **kwargs):
        if self.is_in_group(group) or self.is_in_vgroup(group):
          return f(self, *args, **kwargs)

        raise HTTPError(403, _('You are not allowed to view this ressource'))

      return new_f
    return wrap_f

  def is_finance_admin(self):
    if 'user' in self.session and self.session['user'].is_finance_admin():
      return True

    return False

  def is_admin(self):
    if 'user' in self.session and self.session['user'].is_admin():
      return True

    return False

  def avatarUrl(self, uid, size=20):
    try:
      member = self.mf.getUser(uid)

      if not member.jpegPhoto is None:
        return '/profile/getAvatar/?member_id=' + uid
      else:
        return member.getGravatar(size=size)
    except:
      pass

    return ''

  def pendingMemberValidations(self):
    return self.db.query(TmpMember).count()

  def sendMail(self, to_, subject, body, from_=''):
    msg = MIMEText(body)

    if from_ == '':
      from_ = Config.get('mematool', 'mail_default_from')

    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = to_

    try:
      s = smtplib.SMTP('localhost')
      s.sendmail(from_, [to_], msg.as_string())
      s.quit()
    except:
      if self.debug:
        print 'Error sending mail'
      else:
        raise
