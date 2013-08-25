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
from mako.lookup import TemplateLookup
import ldap
import smtplib
from email.mime.text import MIMEText
from mematool import Config
from mematool.helpers.ldapConnector import LdapConnector
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model.dbmodel import TmpMember
from mematool.helpers.crypto import decodeAES
from mematool.helpers.i18ntool import ugettext as _


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

    self.ldapcon = None
    self.sidebar = []
    self.languages = Config.get('mematool', 'languages', [])
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

  @property
  def db(self):
    return cherrypy.request.db

  @property
  def request(self):
    return cherrypy.request

  def set_ldapcon(self, ldapcon):
    self.ldapcon = ldapcon

  def get_ldapcon(self):
    #@todo: this is not enough ... ass a cherrypy before-handler
    if self.session.get('username') is None or self.session.get('password') is None:
      raise HTTPRedirect('/')

    if self.ldapcon is None:
      username = self.session.get('username')
      password = decodeAES(self.session.get('password'))
      self.ldapcon = LdapConnector(username, password).get_connection()
    else:
      try:
        self.ldapcon.whoami_s()
      except ldap.SERVER_DOWN:
        #@todo make this cleaner refactor
        username = self.session.get('username')
        password = decodeAES(self.session.get('password'))
        self.ldapcon = LdapConnector(username, password).get_connection()

    return self.ldapcon

  def get_ldapMF(self):
    return LdapModelFactory(self.get_ldapcon())

  @property
  def mf(self):
    return self.get_ldapMF()

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
