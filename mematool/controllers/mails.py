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
from mematool.controllers import BaseController, TemplateContext
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker, InvalidParameterFormat
from mematool.model.ldapmodel import Alias

log = logging.getLogger(__name__)


class MailsController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(MailsController, self).__init__()

  def _sidebar(self):
    self.sidebar = []
    self.sidebar.append({'name': _('Show all domains'), 'args': {'controller': 'mails', 'action': 'listDomains'}})
    self.sidebar.append({'name': _('Add domain'), 'args': {'controller': 'mails', 'action': 'editDomain'}})
    self.sidebar.append({'name': _('Add alias'), 'args': {'controller': 'mails', 'action': 'editAlias'}})

  @cherrypy.expose()
  def index(self, msg=None, msg_class='error'):
    if not self.is_admin():
      raise HTTPRedirect('/profile/index')

    if msg and not 'msg' in cherrypy.request.params:
      self.session['flash'] = msg
      self.session['flash_class'] = msg_class
      self.session.save()

    return self.listDomains()

  @cherrypy.expose()
  @BaseController.needAdmin
  def listDomains(self):
    c = TemplateContext()
    c.heading = _('Managed domains')
    c.domains = self.mf.getDomains()

    return self.render('/mails/listDomains.mako', template_context=c)

  @cherrypy.expose()
  @BaseController.needAdmin
  def editDomain(self, domain=None):
    c = TemplateContext()
    # vary form depending on mode (do that over ajax)
    if domain is None:
      action = 'Adding'
      c.mode = 'add'
    else:
      try:
        ParamChecker.checkDomain('domain')
      except:
        return self.index()

      action = 'Editing'
      c.mode = 'edit'
      try:
        c.domain = self.mf.getDomain(domain)
      except LookupError:
        msg = _('No such domain!')
        return self.index(msg=msg)

    c.heading = '%s domain' % (action)

    return self.render('/mails/editDomain.mako', template_context=c)

  def checkEditDomain(f):
    def new_f(self, domain):
      formok = True
      errors = []
      items = {}

      try:
        ParamChecker.checkDomain('domain')
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

        raise HTTPRedirect('/mails/editDomain')
      else:
        items['domain'] = domain

      return f(self, items)
    return new_f

  @cherrypy.expose()
  @BaseController.needAdmin
  @checkEditDomain
  @cherrypy.tools.allow(methods=['POST'])
  def doEditDomain(self, items):
    if not self.mf.addDomain(items['domain']):
      msg = _('Failed to add domain!')
      msg_class = 'error'
    else:
      msg = _('Domain added')
      msg_class = 'success'

    return self.index(msg=msg, msg_class=msg_class)

  @cherrypy.expose()
  @BaseController.needAdmin
  def deleteDomain(self, domain):
    return 'HARD disabled ... you do not want to mess with this in production!!!'

    try:
      ParamChecker.checkDomain('domain', param=True)
    except:
      raise HTTPRedirect('/mails/index')

    try:
      result = self.mf.deleteDomain(domain)

      if result:
        msg = _('Domain successfully deleted')
        msg_class = 'success'
      else:
        msg = _('Failed to delete domain!')
        msg_class = 'error'
    except:
      msg = _('Failed to delete domain!')
      msg_class = 'error'

    self.session.save()
    return self.index(msg=msg, msg_class=msg_class)

  @cherrypy.expose()
  @BaseController.needAdmin
  def listAliases(self, domain, *args, **kwargs):
    try:
      ParamChecker.checkDomain('domain', param=True)
    except:
      raise HTTPRedirect('/mails/index')

    c = TemplateContext()
    c.heading = _('Aliases for domain: %s') % (domain)
    c.domain = domain
    c.aliases = self.mf.getAliases(domain)

    return self.render('/mails/listAliases.mako', template_context=c)

  @cherrypy.expose()
  @BaseController.needAdmin
  def editAlias(self, alias=None, *args, **kwargs):
    c = TemplateContext()

    # vary form depending on mode (do that over ajax)
    if alias is None:
      action = 'Adding'
      c.mode = 'add'

      domains = self.mf.getDomains()
      c.select_domains = []
      for d in domains:
        c.select_domains.append([d.dc, d.dc])

    elif not alias == '':
      try:
        ParamChecker.checkEmail('alias')
      except:
        raise HTTPRedirect('/mails/index')

      action = 'Editing'
      c.alias = alias
      c.mode = 'edit'
      try:
        alias = self.mf.getAlias(alias)
        mail = ''

        for m in alias.mail:
          if not mail == '':
            mail += '\n'
          if not m == alias.dn_mail:
            mail += m

        c.mail = mail

        maildrop = ''

        for m in alias.maildrop:
          if not maildrop == '':
            maildrop += '\n'
          if not m == alias.dn_mail and not m in maildrop:
            maildrop += m

        c.maildrop = maildrop

      except LookupError:
        # @TODO implement better handler
        msg = _('No such alias!')
        return self.index(msg=msg)
    else:
      raise HTTPRedirect('/mails/index')

    c.heading = '{0} alias'.format(action)

    return self.render('/mails/editAlias.mako', template_context=c)

  def checkEditAlias(f):
    def new_f(self, mode, alias, domain, mail=None, maildrop=None):
      formok = True
      errors = []
      items = {}

      if not mode in ['add', 'edit']:
        raise HTTPRedirect('/mails/index')

      if mode == 'add':
        try:
          ParamChecker.checkDomain('domain')
        except InvalidParameterFormat as ipf:
          formok = False
          errors.append(ipf.message)

        alias += '@' + domain

      domain = alias.split('@')[1]

      try:
        ParamChecker.checkDomain(domain, param=False)
      except InvalidParameterFormat as ipf:
        formok = False
        errors.append(ipf.message)

      # @TODO improve check
      try:
        ParamChecker.checkString('maildrop', min_len=0, max_len=300)
      except InvalidParameterFormat as ipf:
        formok = False
        errors.append(_('Invalid mail destination!'))

      if mail and not mail == '':
        for k in mail.split('\n'):
          m = k.replace('\r', '').replace(' ', '')
          if m == '':
            continue

          try:
            ParamChecker.checkEmail(m, param=False)
          except:
            formok = False
            break

          m_domain = m.split('@')[1]
          if not m_domain == domain:
            formok = False
            errors.append(_('All aliases need to be within the same domain!'))
            break

        if len(mail) > 300:
          formok = False

        if not formok:
          errors.append(_('Invalid related aliases!'))

      if not formok:
        self.session['errors'] = errors
        self.session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in cherrypy.request.params.iterkeys():
          self.session['reqparams'][k] = cherrypy.request.params[k]

        self.session.save()

        if mode == 'edit':
          raise HTTPRedirect('/mails/editAlias/?alias={0}'.format(alias))
        else:
          raise HTTPRedirect('/mails/editAlias')
      else:
        items['mode'] = mode
        items['alias'] = alias
        items['mail'] = []
        items['maildrop'] = []

        if mail and len(mail) > 0:
          for k in mail.split('\n'):
            m = k.replace('\r', '').replace(' ', '')
            if m == '':
              continue

            items['mail'].append(m)

        if maildrop and len(maildrop) > 0:
          for k in maildrop.split('\n'):
            m = k.replace('\r', '').replace(' ', '')
            if m == '':
              continue

            items['maildrop'].append(m)

      return f(self, items)
    return new_f

  @cherrypy.expose()
  @BaseController.needAdmin
  @checkEditAlias
  @cherrypy.tools.allow(methods=['POST'])
  def doEditAlias(self, items, *args, **kwargs):
    try:
      alias = Alias()
      alias.dn_mail = items['alias']
      alias.mail = items['mail']
      alias.maildrop = items['maildrop']

      if items['mode'] == 'edit':
        self.mf.updateAlias(alias)
      else:
        self.mf.addAlias(alias)

      self.session['flash'] = _('Alias successfully edited')
      self.session.save()
    except Exception as e:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      msg = _('Error while editing alias')
      return self.index(msg=msg)

    raise HTTPRedirect('/mails/editAlias/?alias={0}'.format(alias.dn_mail))

  @cherrypy.expose()
  @BaseController.needAdmin
  def deleteAlias(self, alias, *args, **kwargs):
    try:
      ParamChecker.checkEmail('alias', param=True)
    except:
      raise HTTPRedirect('/mails/index')

    try:
      result = self.mf.deleteAlias(alias)

      if result:
        msg = _('Alias successfully deleted')
        msg_class = 'success'
      else:
        msg = _('Failed to delete alias!')
        msg_class = 'error'
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      msg = _('Failed to delete alias!')
      msg_class = 'error'

    return self.index(msg=msg, msg_class=msg_class)
