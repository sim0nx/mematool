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

from mematool.lib.base import BaseController, render, Session
from mematool.model import Group

import re
from mematool.lib.syn2cat import regex

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from webob.exc import HTTPUnauthorized
from datetime import date
from mematool.model.ldapModelFactory import LdapModelFactory

# Decorators
from pylons.decorators import validate
from pylons.decorators.rest import restrict

import dateutil.parser
import datetime

import gettext
_ = gettext.gettext


class GroupsController(BaseController):
	def __init__(self):
		super(GroupsController, self).__init__()
		self.lmf = LdapModelFactory()

		c.actions = list()
		c.actions.append((_('Show all groups'), 'groups', 'listGroups'))
		c.actions.append((_('Add Group'), 'groups', 'editGroup'))
		c.actions.append((_('Members'), 'members', 'index'))


	def __before__(self, action, **param):
		super(GroupsController, self).__before__()

	def _require_auth(self):
		return True

	def index(self):
		if self.lmf.isUserInGroup(self.identity, 'office'):
			return self.listGroups()

		return redirect(url(controller='profile', action='index'))

	@BaseController.needAdmin
	def listGroups(self):
		c.heading = _('Managed groups')

		groups_q = Session.query(Group).order_by(Group.gid)
		c.groups = groups_q.all()

		return render('/groups/listGroups.mako')


	@BaseController.needAdmin
	def editGroup(self):
		# vary form depending on mode (do that over ajax)
		if not 'gid' in request.params or request.params['gid'] == '':
			c.group = Group()
			action = 'Adding'
			c.gid = ''
		elif not request.params['gid'] == '' and len(request.params['gid']) > 0:
			action = 'Editing'
			c.gid = request.params['gid']
			group_q = Session.query(Group).filter(Group.gid == request.params['gid'])
			try:
				c.group = group_q.one()

				try:
					lgrp_members = self.lmf.getGroupMembers(request.params['gid'])
					c.group.members = ''

					for k in lgrp_members:
						if not c.group.members == '':
							c.group.members += '\n'

						c.group.members += k
				except LookupError:
					# @TODO implement better handler
					print 'No such group!'
					redirect(url(controller='groups', action='index'))

			except NoResultFound:
				print "oops"
				redirect(url(controller='groups', action='index'))
		else:
			redirect(url(controller='groups', action='index'))

		c.heading = '%s group' % (action)

		return render('/groups/editGroup.mako')

	def checkEdit(f):
		def new_f(self):
			if (not 'gid' in request.params):
				redirect(url(controller='groups', action='index'))
			else:
				formok = True
				errors = []
				items = {}

				if not self._isParamStr('gid', max_len=64):
					formok = False
					print request.params['gid']
					errors.append(_('Invalid group ID'))

				if 'members' in request.params:
					if not self._isParamStr('members') or not re.match(r'([\w]{1,20}\n?)*', request.params['members'], re.I):
						formok = False
						errors.append(_('Invalid group names'))
					else:
						items['members'] = request.params['members']

				if not formok:
					session['errors'] = errors
					session['reqparams'] = {}

					# @TODO request.params may contain multiple values per key... test & fix
					for k in request.params.iterkeys():
						session['reqparams'][k] = request.params[k]
						
					session.save()

					redirect(url(controller='groups', action='editGroup'))
				else:
					items['gid'] = request.params['gid']


			return f(self, items)
		return new_f


	@BaseController.needAdmin
	@checkEdit
	@restrict('POST')
	def doEditGroup(self, items):
		if not self.lmf.addGroup(items['gid']):
			session['flash'] = _('Failed to add group!')
			session['flash_class'] = 'error'
			session.save()
		else:
			if 'members' in items and len(items['members']) > 0:
				form_members = []
				for k in items['members'].split('\n'):
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

			# @TODO add group if not exist

			session['flash'] = _('Group saved successfully')
			session['flash_class'] = 'success'
			session.save()

		redirect(url(controller='groups', action='index'))

	@BaseController.needAdmin
	def unmanageGroup(self):
		if not self._isParamStr('gid'):
			redirect(url(controller='groups', action='index'))

		try:
			g = Session.query(Group).filter(Group.gid == request.params['gid']).one()
			Session.delete(g)
			Session.commit()
		except:
			''' Don't care '''
			pass

		redirect(url(controller='groups', action='index'))

	@BaseController.needAdmin
	def deleteGroup(self):
		if not self._isParamStr('gid'):
			redirect(url(controller='groups', action='index'))

		result = self.lmf.deleteGroup(request.params['gid'])

		if result:
			session['flash'] = _('Group successfully deleted')
			session['flash_class'] = 'success'
		else:
			session['flash'] = _('Failed to delete group!')
			session['flash_class'] = 'error'

		session.save()

		redirect(url(controller='groups', action='index'))
