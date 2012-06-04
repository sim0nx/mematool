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
from pylons.controllers.util import redirect
from pylons import config
from pylons.i18n.translation import _, set_lang
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from datetime import date, datetime

from mematool.lib.base import BaseController, render, Session
from mematool.model import Preferences

log = logging.getLogger(__name__)

import re
from mematool.lib.syn2cat import regex
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat


class PreferencesController(BaseController):
  def __init__(self):
    super(PreferencesController, self).__init__()
    self.lmf = LdapModelFactory()

  def __before__(self):
    super(PreferencesController, self).__before__()
    self._sidebar()

  def _sidebar(self):
    c.actions = list()
    c.actions.append((_('Profile'), 'profile', 'edit'))
    c.actions.append((_('Payments'), 'payments', 'listPayments', session['identity']))

  def index(self):
    return self.edit()

  def edit(self):
    c.heading = _('Edit preferences')
    c.formDisabled = ''

    try:
      member = self.lmf.getUser(session['identity'])
      c.member = member
      pref = Session.query(Preferences).filter(Preferences.uidNumber == member.uidNumber).all()

      c.language = 'en'

      if len(pref) > 0:
        for p in pref:
          if p.key == 'language':
            c.language = p.value

      c.languages = self.languages

      return render('preferences/edit.mako')

    except LookupError:
      print 'Edit :: No such user !'

    return 'ERROR 4x0'

  def checkPreferences(f):
    def new_f(self):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      try:
        ParamChecker.checkString('language', min_len=2, max_len=2)
      except InvalidParameterFormat:
        checkOK = False
        errors.append(_('Invalid language'))

      if not formok:
        session['errors'] = errors
        session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in request.params.iterkeys():
          session['reqparams'][k] = request.params[k]

        session.save()

        redirect(url(controller='preferences', action='edit'))

      return f(self)
    return new_f

  @checkPreferences
  def doEdit(self):
    member = self.lmf.getUser(session['identity'])

    try:
      language = Session.query(Preferences).filter(and_(Preferences.uidNumber == member.uidNumber, Preferences.key == 'language')).one()
      language.last_change = datetime.now()
      language.value = request.params['language']

      session['language'] = language.value
      session['flash'] = _('Changes saved!')
      session['flash_class'] = 'success'
    except NoResultFound:
      pref = Preferences()
      pref.uidNumber = member.uidNumber
      pref.last_change = datetime.now().date()
      pref.key = 'language'
      pref.value = request.params['language']
      Session.add(pref)

      session['language'] = request.params['language']

      session['flash'] = _('Changes saved!')
      session['flash_class'] = 'success'
    except:
      session['flash'] = _('Unknown error, nothing saved')
      session['flash_class'] = 'error'

    Session.commit()

    session.save()
    redirect(url(controller='preferences', action='edit'))
