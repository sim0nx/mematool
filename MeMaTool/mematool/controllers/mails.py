# -*- coding: utf-8 -*-
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
log = logging.getLogger(__name__)

from pylons import request, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons.i18n.translation import _

from mematool.lib.base import BaseController, render

from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model import Alias
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat

# Decorators
from pylons.decorators.rest import restrict
from webhelpers.html.builder import literal


class MailsController(BaseController):
  def __init__(self):
    super(MailsController, self).__init__()
    self.lmf = LdapModelFactory()

  def __before__(self, action, **param):
    super(MailsController, self).__before__()

  def _sidebar(self):
    super(MailsController, self)._sidebar()

    c.actions.append({'name' : _('Show all domains'), 'args' : {'controller' : 'mails', 'action' : 'listDomains'}})
    c.actions.append({'name' : _('Add domain'), 'args' : {'controller' : 'mails', 'action' : 'editDomain'}})
    c.actions.append({'name' : _('Add alias'), 'args' : {'controller' : 'mails', 'action' : 'editAlias'}})

  def index(self):
    if self.lmf.isUserInGroup(self.identity, 'office') or self.lmf.isUserInGroup(self.identity, 'sysops'):
      return self.listDomains()

    return redirect(url(controller='profile', action='index'))

  @BaseController.needAdmin
  def listDomains(self):
    c.heading = _('Managed domains')

    c.domains = self.lmf.getDomains()

    return render('/mails/listDomains.mako')

  @BaseController.needAdmin
  def editDomain(self):
    # vary form depending on mode (do that over ajax)
    if not 'domain' in request.params or request.params['domain'] == '':
      action = 'Adding'
      c.mode = 'add'
    else:
      try:
        ParamChecker.checkDomain('domain')
      except:
        redirect(url(controller='mails', action='index'))

      action = 'Editing'
      c.mode = 'edit'
      try:
        c.domain = self.lmf.getDomain(request.params['domain'])
      except LookupError:
        # @TODO implement better handler
        print 'No such domain!'
        redirect(url(controller='mails', action='index'))

    c.heading = '%s domain' % (action)

    return render('/mails/editDomain.mako')

  def checkEditDomain(f):
    def new_f(self):
      if (not 'domain' in request.params):
        redirect(url(controller='mails', action='index'))
      else:
        formok = True
        errors = []
        items = {}

        try:
          ParamChecker.checkDomain('domain')
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

          redirect(url(controller='mails', action='editDomain'))
        else:
          items['domain'] = request.params['domain']

      return f(self, items)
    return new_f

  @BaseController.needAdmin
  @checkEditDomain
  @restrict('POST')
  def doEditDomain(self, items):
    if not self.lmf.addDomain(items['domain']):
      session['flash'] = _('Failed to add domain!')
      session['flash_class'] = 'error'
      session.save()

    redirect(url(controller='mails', action='index'))

  @BaseController.needAdmin
  def deleteDomain(self):
    return 'HARD disabled ... you do not want to mess with this in production!!!'

    try:
      ParamChecker.checkDomain('domain', param=True)
    except:
      redirect(url(controller='mails', action='index'))

    try:
      result = self.lmf.deleteDomain(request.params['domain'])

      if result:
        session['flash'] = _('Domain successfully deleted')
        session['flash_class'] = 'success'
      else:
        session['flash'] = _('Failed to delete domain!')
        session['flash_class'] = 'error'
    except:
      session['flash'] = _('Failed to delete domain!')
      session['flash_class'] = 'error'

    session.save()
    redirect(url(controller='mails', action='index'))

  @BaseController.needAdmin
  def listAliases(self):
    try:
      ParamChecker.checkDomain('domain', param=True)
    except:
      redirect(url(controller='mails', action='index'))

    c.heading = _('Aliases for domain: %s') % (request.params['domain'])
    c.domain = request.params['domain']
    c.aliases = self.lmf.getAliases(request.params['domain'])

    return render('/mails/listAliases.mako')

  @BaseController.needAdmin
  def editAlias(self):
    # vary form depending on mode (do that over ajax)
    if not 'alias' in request.params or request.params['alias'] == '':
      action = 'Adding'
      c.mode = 'add'

      domains = self.lmf.getDomains()
      c.select_domains = []
      for d in domains:
        c.select_domains.append([d.dc, d.dc])

    elif not request.params['alias'] == '':
      try:
        ParamChecker.checkEmail('alias')
      except:
        redirect(url(controller='mails', action='index'))

      action = 'Editing'
      c.alias = request.params['alias']
      c.mode = 'edit'
      try:
        alias = self.lmf.getAlias(request.params['alias'])
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
        print 'No such alias!'
        redirect(url(controller='mails', action='index'))
    else:
      redirect(url(controller='mails', action='index'))

    c.heading = '%s alias' % (action)

    onclick = literal("return confirm('Are you sure you want to delete \\'{0}\\'?')".format(request.params.get('alias')))
    c.actions.append({'name' : _('Delete alias'), 'onclick' : onclick, 'args' : {'controller' : 'mails', 'action' : 'deleteAlias', 'alias' : request.params.get('alias')}})

    return render('/mails/editAlias.mako')

  def checkEditAlias(f):
    def new_f(self):
      if (not 'mode' in request.params) or (not 'alias' in request.params) or (not 'domain' in request.params):
        redirect(url(controller='mails', action='index'))
      else:
        formok = True
        errors = []
        items = {}

        mode = request.params['mode']
        if not mode == 'add' and not mode == 'edit':
          redirect(url(controller='mails', action='index'))

        if mode == 'add':
          try:
            ParamChecker.checkDomain('domain')
          except InvalidParameterFormat as ipf:
            formok = False
            errors.append(ipf.message)

          alias = request.params['alias'] + '@' + request.params['domain']
        else:
          alias = request.params['alias']

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

        if 'mail' in request.params and not request.params['mail'] == '':
          for k in request.params['mail'].split('\n'):
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

          if len(request.params['mail']) > 300:
            formok = False

          if not formok:
            errors.append(_('Invalid related aliases!'))

        if not formok:
          session['errors'] = errors
          session['reqparams'] = {}

          # @TODO request.params may contain multiple values per key... test & fix
          for k in request.params.iterkeys():
            session['reqparams'][k] = request.params[k]

          session.save()

          if mode == 'edit':
            redirect(url(controller='mails', action='editAlias', alias=alias))
          else:
            redirect(url(controller='mails', action='editAlias'))
        else:
          items['mode'] = mode
          items['alias'] = alias
          items['mail'] = []
          items['maildrop'] = []

          if 'mail' in request.params and len(request.params['mail']) > 0:
            for k in request.params['mail'].split('\n'):
              m = k.replace('\r', '').replace(' ', '')
              if m == '':
                continue

              items['mail'].append(m)

          if 'maildrop' in request.params and len(request.params['maildrop']) > 0:
            for k in request.params['maildrop'].split('\n'):
              m = k.replace('\r', '').replace(' ', '')
              if m == '':
                continue

              items['maildrop'].append(m)

      return f(self, items)
    return new_f

  @BaseController.needAdmin
  @checkEditAlias
  @restrict('POST')
  def doEditAlias(self, items):
    try:
      alias = Alias()
      alias.dn_mail = items['alias']
      alias.mail = items['mail']
      alias.maildrop = items['maildrop']

      if items['mode'] == 'edit':
        self.lmf.updateAlias(alias)
      else:
        self.lmf.addAlias(alias)

      session['flash'] = _('Alias successfully edited')
      session.save()
    except Exception as e:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      session['flash'] = _('Error while editing alias')
      session.save()
      redirect(url(controller='mails', action='index'))

    redirect(url(controller='mails', action='editAlias', alias=alias.dn_mail))
    #redirect(url(controller='mails', action='listAliases', domain=alias.domain))

  @BaseController.needAdmin
  def deleteAlias(self):
    try:
      ParamChecker.checkEmail('alias', param=True)
    except:
      redirect(url(controller='mails', action='index'))

    try:
      result = self.lmf.deleteAlias(request.params['alias'])

      if result:
        session['flash'] = _('Alias successfully deleted')
        session['flash_class'] = 'success'
      else:
        session['flash'] = _('Failed to delete alias!')
        session['flash_class'] = 'error'
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      session['flash'] = _('Failed to delete alias!')
      session['flash_class'] = 'error'

    session.save()
    redirect(url(controller='mails', action='index'))
