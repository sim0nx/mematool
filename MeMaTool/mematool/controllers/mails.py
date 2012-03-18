#
#    MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
#    This file is part of MeMaTool.
#
#
#    MeMaTool is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.

import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from mematool.lib.base import BaseController, render

import re
from mematool.lib.syn2cat import regex

from datetime import date
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model import Group

# Decorators
from pylons.decorators import validate
from pylons.decorators.rest import restrict

import dateutil.parser
import datetime

import gettext
_ = gettext.gettext


class MailsController(BaseController):
	def __init__(self):
		super(MailsController, self).__init__()
		self.lmf = LdapModelFactory()

		c.actions = list()
		c.actions.append((_('Show all domains'), 'mails', 'listDomains'))
		c.actions.append((_('Add domain'), 'mails', 'editDomain'))

	def __before__(self, action, **param):
		super(MailsController, self).__before__()

	def _require_auth(self):
		return True

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
		if not 'gid' in request.params or request.params['gid'] == '':
			c.mail = Group()
			action = 'Adding'
			c.gid = ''
		elif not request.params['gid'] == '' and len(request.params['gid']) > 0:
			action = 'Editing'
			c.gid = request.params['gid']
			try:
				c.mail = self.lmf.getGroup(request.params['gid'])
				users = ''

				for u in c.mail.users:
					if not users == '':
						users += '\n'
					users += u

				c.mail.users = users
			except LookupError:
				# @TODO implement better handler
				print 'No such mail!'
				redirect(url(controller='mail', action='index'))
		else:
			redirect(url(controller='mail', action='index'))

		c.heading = '%s mail' % (action)

		return render('/mail/editGroup.mako')

	def checkEdit(f):
		def new_f(self):
			if (not 'gid' in request.params):
				redirect(url(controller='mail', action='index'))
			else:
				formok = True
				errors = []
				items = {}

				if not self._isParamStr('gid', max_len=64):
					formok = False
					print request.params['gid']
					errors.append(_('Invalid mail ID'))

				if 'users' in request.params:
					if not self._isParamStr('users') or not re.match(r'([\w]{1,20}\n?)*', request.params['users'], re.I):
						formok = False
						errors.append(_('Invalid mail names'))
					else:
						items['users'] = request.params['users']

				if not formok:
					session['errors'] = errors
					session['reqparams'] = {}

					# @TODO request.params may contain multiple values per key... test & fix
					for k in request.params.iterkeys():
						session['reqparams'][k] = request.params[k]
						
					session.save()

					redirect(url(controller='mail', action='editGroup'))
				else:
					items['gid'] = request.params['gid']


			return f(self, items)
		return new_f


	@BaseController.needAdmin
	@checkEdit
	@restrict('POST')
	def doEditGroup(self, items):
		if not self.lmf.addGroup(items['gid']):
			session['flash'] = _('Failed to add mail!')
			session['flash_class'] = 'error'
			session.save()
		else:
			if 'users' in items and len(items['users']) > 0:
				form_members = []
				for k in items['users'].split('\n'):
					m = k.replace('\r', '').replace(' ', '')
					if m == '':
						continue

					form_members.append(m)

				if len(form_members) > 0:
					try:
						lgrp_members = self.lmf.getGroupMembers(items['gid'])
					except LookupError:
						lgrp_members = []

					# Adding new members
					for m in form_members:
						if not m in lgrp_members:
							#print 'adding -> ' + str(m)
							self.lmf.changeUserGroup(m, items['gid'], True)

					# Removing members
					for m in lgrp_members:
						if not m in form_members:
							#print 'removing -> ' + str(m)
							self.lmf.changeUserGroup(m, items['gid'], False)

			# @TODO add mail if not exist

			session['flash'] = _('Group saved successfully')
			session['flash_class'] = 'success'
			session.save()

		redirect(url(controller='mail', action='index'))

	@BaseController.needAdmin
	def listAliases(self):
		if not self._isParamStr('domain'):
			redirect(url(controller='mail', action='index'))

		c.heading = _('Aliases for domain: %s') % (request.params['domain'])
		c.domain = request.params['domain']
		c.aliases = self.lmf.getAliases(request.params['domain'])

		return render('/mails/listAliases.mako')

	@BaseController.needAdmin
	def editAlias(self):
		# vary form depending on mode (do that over ajax)
		if not 'alias' in request.params or request.params['alias'] == '':
			c.alias = Alias()
			action = 'Adding'
			c.alias = ''
		elif not request.params['alias'] == '':
			action = 'Editing'
			c.alias = request.params['alias']
			try:
				c.alias = self.lmf.getAlias(request.params['alias'])
				mails = ''

				for m in c.alias.mail:
					if not mails == '':
						mails += '\n'
					mails += m

				c.alias.mails = mails
			except LookupError:
				# @TODO implement better handler
				print 'No such alias!'
				redirect(url(controller='mails', action='index'))
		else:
			redirect(url(controller='mails', action='index'))

		c.heading = '%s alias' % (action)

		return render('/mails/editAlias.mako')


	@BaseController.needAdmin
	def deleteGroup(self):
		if not self._isParamStr('gid'):
			redirect(url(controller='mail', action='index'))

		result = self.lmf.deleteGroup(request.params['gid'])

		if result:
			session['flash'] = _('Group successfully deleted')
			session['flash_class'] = 'success'
		else:
			session['flash'] = _('Failed to delete mail!')
			session['flash_class'] = 'error'

		session.save()

		redirect(url(controller='mail', action='index'))
