#
# MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
# This file is part of MeMaTool.
#
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member, TmpMember

log = logging.getLogger(__name__)

import re
from mematool.lib.syn2cat import regex
from mematool.lib.syn2cat.crypto import encodeAES
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat

from webob.exc import HTTPUnauthorized

import gettext
_ = gettext.gettext



class ProfileController(BaseController):

  def __init__(self):
    super(ProfileController, self).__init__()
    self.lmf = LdapModelFactory()

  def __before__(self):
    super(ProfileController, self).__before__()

    if not self.identity:
      redirect(url(controller='error', action='forbidden'))


  def _require_auth(self):
    return True


  def index(self):
    return self.edit()


  def edit(self):
    c.heading = _('Edit profile')
    c.formDisabled = ''

    try:
      member = self.lmf.getUser(session['identity'])

      if member.validate:
        tm = Session.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        member.cn = tm.gn + ' ' + tm.sn
        member.givenName = tm.gn
        member.sn = tm.sn
        member.birthDate = tm.birthDate
        member.homePostalAddress = tm.homePostalAddress
        member.homePhone = tm.phone
        member.mobile = tm.mobile
        member.mail = tm.mail
        member.xmppID = tm.xmppID

        c.formDisabled = 'disabled'

      c.member = member

      if member.fullMember:
        c.member.full_member = True
      else:
        c.member.full_member = False
      if member.lockedMember:
        c.member.locked_member = True
      else:
        c.member.locked_member = False

      c.actions = list()
      c.actions.append( (_('Payments'), 'payments', 'listPayments', session['identity']) )


      return render('/profile/edit.mako')

    except LookupError:
      print 'Edit :: No such user !'


    return 'ERROR 4x0'


  def checkMember(f):
    def new_f(self):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      m = self.lmf.getUser(session['identity'])

      for v in m.str_vars:
        if v in request.params:
          setattr(m, v, request.params.get(v, ''))

      try:
        m.check()
      except InvalidParameterFormat as ipf:
        formok = False
        errors += ipf.message

      if 'userPassword' in request.params and len(request.params['userPassword']) > 0:
        try:
          ParamChecker.checkPassword('userPassword', 'userPassword2')
        except InvalidParameterFormat as ipf:
          formok = False
          errors.append(ipf.message)

      if not formok:
        session['errors'] = errors
        session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in request.params.iterkeys():
          session['reqparams'][k] = request.params[k]

        session.save()

        redirect(url(controller='profile', action='edit'))

      return f(self)
    return new_f


  @checkMember
  def doEdit(self):
    m = self.lmf.getUser(session['identity'])

    if m.validate:
      # member locked for validation
      redirect(url(controller='error', action='forbidden'))
    else:
      changes = False

      if request.params['sn'] != m.sn or\
        request.params['givenName'] != m.givenName or\
        request.params['birthDate'] != m.birthDate or\
        request.params['homePostalAddress'] != m.homePostalAddress or\
        ('homePhone' in request.params and len(request.params['homePhone']) > 0 and request.params['homePhone'] != m.homePhone) or\
        request.params['mobile'] != m.mobile or\
        request.params['mail'] != m.mail or\
        request.params['xmppID'] != m.xmppID:
        changes = True

      if changes:
        tm = TmpMember(m.uidNumber)
        tm.sn = str(request.params['sn'].encode('utf-8'))
        tm.gn = str(request.params['givenName'].encode('utf-8'))
        tm.birthDate = request.params['birthDate']
        tm.homePostalAddress = str(request.params['homePostalAddress'].encode('utf-8'))

        if 'homePhone' not in request.params or (request.params['homePhone'] == '' and not m.homePhone is ''):
          tm.phone = '>>REMOVE<<'
        else:
          tm.phone = request.params['homePhone']

        if 'xmppID' not in request.params or (request.params['xmppID'] == '' and not m.xmppID is ''):
          tm.xmppID = 'removed'
        else:
          tm.xmppID = request.params['xmppID']

        tm.mobile = request.params['mobile']
        tm.mail = request.params['mail']

        Session.add(tm)
        Session.commit()

        session['flash'] = _('Changes saved!')
        session['flash_class'] = 'success'
      else:
        session['flash'] = _('Nothing to save!')
        session['flash_class'] = 'info'


      if 'userPassword' in request.params and 'userPassword2' in request.params and request.params['userPassword'] != '' and request.params['userPassword'] == request.params['userPassword2']:
        m.setPassword(request.params['userPassword'])
        self.lmf.saveMember(m)
        session['secret'] = encodeAES(request.params['userPassword'])

        session['flash'] = _('Password updated!')
        session['flash_class'] = 'success'
    
    session.save()
    redirect(url(controller='profile', action='index'))
