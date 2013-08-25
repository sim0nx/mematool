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
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
import datetime
from mematool import Config
from mematool.controllers import BaseController, TemplateContext
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker, InvalidParameterFormat
from mematool.model.dbmodel import Preferences

log = logging.getLogger(__name__)


class PreferencesController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(PreferencesController, self).__init__()

  def _sidebar(self):
    self.sidebar = []
    self.sidebar.append({'name': _('Profile'), 'args': {'controller': 'profile', 'action': 'edit'}})
    self.sidebar.append({'name': _('Payments'), 'args': {'controller': 'payments', 'action': 'listPayments', 'params': {'member_id': self.session.get('username')}}})

  @cherrypy.expose()
  def index(self):
    return self.edit()

  @cherrypy.expose()
  def edit(self):
    c = TemplateContext()
    c.heading = _('Edit preferences')
    c.formDisabled = ''

    try:
      member = self.session.get('user')
      c.member = member
      pref = self.db.query(Preferences).filter(Preferences.uidNumber == member.uidNumber).all()

      c.language = 'en'

      if len(pref) > 0:
        for p in pref:
          if p.key == 'language':
            c.language = p.value

      c.languages = Config.get('mematool', 'languages', ['en'])

      return self.render('preferences/edit.mako', template_context=c)

    except LookupError:
      print 'Edit :: No such user !'

    return 'ERROR 4x0'

  def checkPreferences(f):
    def new_f(self, language):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      try:
        ParamChecker.checkString('language', min_len=2, max_len=2)
      except InvalidParameterFormat:
        errors.append(_('Invalid language'))

      if not formok:
        self.session['errors'] = errors
        self.session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in self.request.params.iterkeys():
          self.session['reqparams'][k] = self.request.params[k]

        self.session.save()

        raise HTTPRedirect('/preferences/edit')

      return f(self)
    return new_f

  @cherrypy.expose()
  @checkPreferences
  def doEdit(self):
    member = self.session.get('user')

    try:
      language = self.db.query(Preferences).filter(and_(Preferences.uidNumber == member.uidNumber, Preferences.key == 'language')).one()
      language.last_change = datetime.datetime.now()
      language.value = self.request.params['language']

      self.session['language'] = language.value
      self.session['flash'] = _('Changes saved!')
      self.session['flash_class'] = 'success'
    except NoResultFound:
      pref = Preferences()
      pref.uidNumber = member.uidNumber
      pref.last_change = datetime.datetime.now().date()
      pref.key = 'language'
      pref.value = self.request.params['language']
      self.db.add(pref)

      self.session['language'] = cherrypy.request.params['language']

      self.session['flash'] = _('Changes saved!')
      self.session['flash_class'] = 'success'
    except:
      self.session['flash'] = _('Unknown error, nothing saved')
      self.session['flash_class'] = 'error'

    self.db.commit()

    self.session.save()
    raise HTTPRedirect('/preferences/edit')
