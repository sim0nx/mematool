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
from mematool.model.dbmodel import Group

log = logging.getLogger(__name__)


class GroupsController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(GroupsController, self).__init__()

  def _sidebar(self):
    self.sidebar = []
    self.sidebar.append({'name': _('Show all groups'), 'args': {'controller': 'groups', 'action': 'listGroups'}})
    self.sidebar.append({'name': _('Add Group'), 'args': {'controller': 'groups', 'action': 'editGroup'}})
    self.sidebar.append({'name': _('Members'), 'args': {'controller': 'members', 'action': 'index'}})

  @cherrypy.expose()
  def index(self, msg=None, msg_class='error'):
    if msg and not 'msg' in cherrypy.request.params:
      self.session['flash'] = msg
      self.session['flash_class'] = msg_class
      self.session.save()
    
    if self.is_admin():
      return self.listGroups()

    raise HTTPRedirect('/profile/index')

  @cherrypy.expose()
  @BaseController.needGroup('superadmin')
  def listGroups(self):
    c = TemplateContext()
    c.heading = _('Managed groups')
    c.groups = self.mf.getManagedGroupList()

    return self.render('/groups/listGroups.mako', template_context=c)

  @cherrypy.expose()
  @BaseController.needGroup('superadmin')
  def editGroup(self, gid=None):
    c = TemplateContext()

    # vary form depending on mode (do that over ajax)
    if gid is None:
      c.group = Group()
      action = 'Adding'
      c.gid = ''
    else:
      try:
        ParamChecker.checkUsername('gid', param=True)
      except:
        msg =  _('Invalid format!')
        return self.index(msg=msg)

      action = 'Editing'
      c.gid = gid
      try:
        c.group = self.mf.getGroup(gid)
        print 'poll'
        users = ''

        for u in c.group.users:
          if not users == '':
            users += '\n'
          users += u

        c.group.users = users
      except LookupError:
        # @TODO implement better handler
        msg =  _('No such group!')
        return self.index(msg=msg)

    c.heading = '{0} group'.format(action)

    return self.render('/groups/editGroup.mako', template_context=c)

  def checkEdit(f):
    def new_f(self, gid, users=None):
      formok = True
      errors = []
      items = {}

      try:
        ParamChecker.checkUsername('gid', param=True)
      except:
        formok = False
        errors.append(_('Invalid group ID'))

      items['users'] = []

      if not users is None:
        try:
          #ParamChecker.checkString('users', param=True, min_len=-1, max_len=9999, regex=r'([\w]{1,20}\n?)*')

          for k in users.split('\n'):
            m = k.replace('\r', '').replace(' ', '')
            if m == '':
              continue
            else:
              ParamChecker.checkUsername(m, param=False)
              items['users'].append(m)
        except InvalidParameterFormat as ipf:
          formok = False
          errors.append(_('Invalid user name(s)'))

      if not formok:
        self.session['errors'] = errors
        self.session['reqparams'] = {}

        # @TODO request.params may contain multiple values per key... test & fix
        for k in self.request.params.iterkeys():
          self.session['reqparams'][k] = cherrypy.request.params[k]

        self.session.save()

        raise HTTPRedirect('/groups/editGroup/?gid={0}'.format(gid))
      else:
        items['gid'] = gid

      return f(self, items)
    return new_f

  @cherrypy.expose()
  @cherrypy.tools.allow(methods=['POST'])
  @BaseController.needGroup('superadmin')
  @checkEdit
  def doEditGroup(self, items):
    if not self.mf.addGroup(items['gid']):
      msg = _('Failed to add group!')
      msg_class = 'error'
    else:
      try:
        lgrp_members = self.mf.getGroupMembers(items['gid'])
      except LookupError:
        lgrp_members = []

      # Adding new members
      for m in items['users']:
        if not m in lgrp_members:
          #print 'adding -> ' + str(m)
          self.mf.changeUserGroup(m, items['gid'], True)

      # Removing members
      for m in lgrp_members:
        if not m in items['users']:
          #print 'removing -> ' + str(m)
          self.mf.changeUserGroup(m, items['gid'], False)

      # @TODO add group if not exist

      msg = _('Group saved successfully')
      msg_class = 'success'

    return self.index(msg=msg, msg_class=msg_class)

  @cherrypy.expose()
  @BaseController.needGroup('superadmin')
  def unmanageGroup(self, gid):
    try:
      ParamChecker.checkUsername('gid', param=True)
    except:
      raise HTTPRedirect('/groups/index')

    result = self.mf.unmanageGroup(gid)

    if result:
      msg = _('Group no longer managed')
      msg_class = 'success'
    else:
      msg = _('Failed to remove group from management!')
      msg_class = 'error'

    return self.index(msg=msg, msg_class=msg_class)

  @cherrypy.expose()
  @BaseController.needGroup('superadmin')
  def deleteGroup(self, gid):
    try:
      ParamChecker.checkUsername('gid', param=True)
    except:
      raise HTTPRedirect('/groups/index')

    result = self.mf.deleteGroup(request.params['gid'])

    if result:
      msg = _('Group successfully deleted')
      msg_class = 'success'
    else:
      msg = _('Failed to delete group!')
      msg_class = 'error'

    return self.index(msg=msg, msg_class=msg_class)
