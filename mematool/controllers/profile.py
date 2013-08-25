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
from cherrypy._cperror import HTTPError
import logging
from PIL import Image
import StringIO
import base64
from mematool import Config
from mematool.controllers import BaseController, TemplateContext
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker, InvalidParameterFormat
from mematool.helpers.crypto import encodeAES
from mematool.model.dbmodel import TmpMember
from cherrypy._cperror import HTTPRedirect

log = logging.getLogger(__name__)


class ProfileController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(ProfileController, self).__init__()

  def _sidebar(self):
    self.sidebar = []

    self.sidebar.append({'name': _('Preferences'), 'args': {'controller': 'preferences', 'action': 'edit'}})
    self.sidebar.append({'name': _('Payments'), 'args': {'controller': 'payments', 'action': 'listPayments', 'params': {'member_id': self.session.get('username')}}})

  @cherrypy.expose
  def index(self):
    return self.edit()

  @cherrypy.expose
  def edit(self):
    c = TemplateContext()
    c.heading = _('Edit profile')
    c.formDisabled = ''

    try:
      member = self.mf.getUser(self.session.get('username'))

      if member.validate:
        tm = self.db.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        member.givenName = tm.gn
        member.sn = tm.sn
        member.homePostalAddress = tm.homePostalAddress
        member.homePhone = tm.phone
        member.mobile = tm.mobile
        member.mail = tm.mail
        member.xmppID = tm.xmppID

        c.formDisabled = 'disabled'

      c.member = member
      c.member.avatarUrl = self.avatarUrl(member.uid, size=180)
      c.groups = member.groups
    except LookupError:
      return 'Edit :: No such user !'

    return self.render('/profile/edit.mako', template_context=c)

  def checkMember(f):
    def new_f(self, **kwargs):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      m = self.mf.getUser(self.session.get('username'))

      for v in m.str_vars:
        if v in self.request.params:
          setattr(m, v, self.request.params.get(v, ''))

      try:
        m.check()
      except InvalidParameterFormat as ipf:
        formok = False
        errors += ipf.message

      if not self.request.params.get('userPassword', '') == '' and self.request.params['userPassword'] == self.request.params['userPassword2']:
        try:
          ParamChecker.checkPassword('userPassword', 'userPassword2')
        except InvalidParameterFormat as ipf:
          formok = False
          errors.append(ipf.message)

      if not formok:
        self.session['errors'] = errors
        self.session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in self.request.params.iterkeys():
          self.session['reqparams'][k] = self.request.params[k]

        self.session.save()

        raise HTTPRedirect('/profile/edit')

      return f(self)
    return new_f

  @cherrypy.expose
  @checkMember
  def doEdit(self):
    m = self.mf.getUser(self.session['username'])

    if m.validate:
      # member locked for validation
      raise HTTPError(403, 'Forbidden')
    else:
      changes = False

      if self.request.params['sn'] != m.sn or\
        self.request.params['givenName'] != m.givenName or\
        self.request.params['homePostalAddress'] != m.homePostalAddress or\
        self.request.params['homePhone'] != m.homePhone or\
        self.request.params['mobile'] != m.mobile or\
        self.request.params['mail'] != m.mail or\
        self.request.params['xmppID'] != m.xmppID:
        changes = True

      if changes:
        tm = TmpMember(m.uidNumber)
        tm.sn = str(self.request.params['sn'].encode('utf-8'))
        tm.gn = str(self.request.params['givenName'].encode('utf-8'))
        tm.homePostalAddress = str(self.request.params['homePostalAddress'].encode('utf-8'))

        # @TODO make this more consistent
        if self.request.params.get('homePhone', '') == '' and not m.homePhone == '':
          tm.phone = '>>REMOVE<<'
        else:
          tm.phone = self.request.params['homePhone']

        if self.request.params.get('xmppID', '') == '' and not m.xmppID == '':
          tm.xmppID = 'removed'
        else:
          tm.xmppID = self.request.params['xmppID']

        tm.mobile = self.request.params['mobile']
        tm.mail = self.request.params['mail']

        self.db.add(tm)
        self.db.commit()

        self.session['flash'] = _('Changes saved!')
        self.session['flash_class'] = 'success'

        self.mailValidationRequired()
      else:
        self.session['flash'] = _('Nothing to save!')
        self.session['flash_class'] = 'info'

      if not self.request.params.get('userPassword', '') == '' and self.request.params['userPassword'] == self.request.params['userPassword2']:
        m.setPassword(self.request.params['userPassword'])
        self.mf.saveMember(m, is_admin=False)
        self.session['secret'] = encodeAES(self.request.params['userPassword'])

        self.session['flash'] = _('Password updated!')
        self.session['flash_class'] = 'success'

    self.session.save()
    raise HTTPRedirect('/profile/index')

  def mailValidationRequired(self):
    body = 'Hi,\n'
    body += 'The following user has updated his profile which requires your approval:\n'
    body += self.session['username'] + '\n'
    body += 'Please carefully review his changes and approve or reject them as required.\n\n'
    body += 'regards,\nMeMaTool'

    to = 'office@hackerspace.lu'
    subject = Config.get('mematool', 'name_prefix') + ' mematool - request for validation'
    self.sendMail(to, subject, body)

  def _resizeImage(self, img):
      try:
        o_img = Image.open(img)
        max_size = (240, 240)
        o_img.thumbnail(max_size, Image.ANTIALIAS)

        out = StringIO.StringIO()
        o_img.save(out, format='jpeg', quality=75)

        return base64.b64encode(out.getvalue())
      except:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)

      return None

  @cherrypy.expose
  def editAvatar(self):
    c = TemplateContext()
    c.heading = _('Edit avatar')

    try:
      member = self.mf.getUser(self.session['username'])
      member.avatarUrl = self.avatarUrl(member.uid, size=180)
      c.member = member

      return self.render('/profile/editAvatar.mako', template_context=c)

    except LookupError:
      print 'Edit :: No such user !'

    return 'ERROR 4x0'

  @cherrypy.expose
  @cherrypy.tools.allow(methods=['POST'])
  def doEditAvatar(self):
    if not 'avatar' in self.request.params or not len(self.request.params['avatar'].value) > 0:
      raise HTTPRedirect('/profile/editAvatar')

    try:
      img_param = self.request.params['avatar'].file
      img = self._resizeImage(img_param)
      member = self.mf.getUser(self.session['username'])
      self.mf.updateAvatar(member, img)
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)

    raise HTTPRedirect('/profile/editAvatar')

  @cherrypy.expose
  def doDeleteAvatar(self):
    try:
      member = self.mf.getUser(self.session['username'])
      self.mf.updateAvatar(member, None)
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)

    raise HTTPRedirect('/profile/editAvatar')

  @cherrypy.expose
  def getAvatar(self, member_id):
    try:
      member = self.mf.getUser(member_id)

      if not member.jpegPhoto is None:
        return member.avatar
    except:
      pass

    return '4x4 p0wer'
