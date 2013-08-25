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
from mematool.controllers import BaseController, TemplateContext
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker, InvalidParameterFormat
from mematool.model.dbmodel import TmpMember
from mematool.model.ldapmodel import Member
from mematool import Config

log = logging.getLogger(__name__)


class MembersController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(MembersController, self).__init__()

  def _sidebar(self):
    self.sidebar = []
    self.sidebar.append({'name': _('Show all members'), 'args': {'controller': 'members', 'action': 'showAllMembers'}})
    self.sidebar.append({'name': _('Add member'), 'args': {'controller': 'members', 'action': 'addMember'}})
    self.sidebar.append({'name': _('Active members'), 'args': {'controller': 'members', 'action': 'showActiveMembers'}})
    self.sidebar.append({'name': _('Former members'), 'args': {'controller': 'members', 'action': 'showFormerMembers'}})
    self.sidebar.append({'name': _('Groups'), 'args': {'controller': 'groups', 'action': 'index'}})

  @cherrypy.expose()
  def index(self):
    return self.showAllMembers()

  @cherrypy.expose()
  @BaseController.needAdmin
  def addMember(self):
    c = TemplateContext()
    c.heading = _('Add member')
    c.mode = 'add'
    c.groups = []

    return self.render('/members/editMember.mako', template_context=c)

  @cherrypy.expose()
  @BaseController.needAdmin
  def editMember(self, member_id):
    c = TemplateContext()
    try:
      c.heading = _('Edit member')
      c.member = self.mf.getUser(member_id)
      c.mode = 'edit'

      return self.render('/members/editMember.mako', template_context=c)

    except LookupError:
      print 'No such user !'

    return 'ERROR 4x0'

  def checkMember(f):
    def new_f(self, member_id, **kwargs):
      # @TODO request.params may contain multiple values per key... test & fix
      formok = True
      errors = []

      try:
        ParamChecker.checkMode('mode', values=('add', 'edit'))
      except InvalidParameterFormat as ipf:
        formok = False
        errors.append(ipf.message)

      m = Member()

      for v in m.str_vars:
        setattr(m, v, self.request.params.get(v, ''))

      m.uid = member_id

      try:
        m.check()
      except InvalidParameterFormat as ipf:
        formok = False
        errors += ipf.message

      if self.request.params['mode'] == 'add' or not self.request.params.get('userPassword', '') == '':
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
          if k == 'fullMember' or k == 'lockedMember':
            if self.request.params[k] == 'on':
              self.session['reqparams'][k] = True
            else:
              self.session['reqparams'][k] = False
          else:
            self.session['reqparams'][k] = self.request.params[k]

        self.session.save()

        if self.request.params['mode'] == 'add':
          raise HTTPRedirect('/members/addMember')
        else:
          raise HTTPRedirect('/members/editMember/?member_id={0}'.format(member_id))

      return f(self)
    return new_f

  @cherrypy.expose()
  @cherrypy.tools.allow(methods=['POST'])
  @BaseController.needAdmin
  @checkMember
  def doEditMember(self):
    try:
      if self.request.params['mode'] == 'edit':
        member = self.mf.getUser(self.request.params['member_id'])
      else:
        member = Member()
        member.uid = self.request.params['member_id']

      for v in member.str_vars:
        if v in self.request.params:
          setattr(member, v, self.request.params.get(v).lstrip(' ').rstrip(' '))

      for v in member.bool_vars:
        if v in self.request.params:
          setattr(member, v, True)

      if not self.request.params.get('userPassword', '') == '' and self.request.params['userPassword'] == self.request.params['userPassword2']:
        member.setPassword(self.request.params['userPassword'])

      ''' fullMember / lockedMember'''
      if 'fullMember' in self.request.params and not Config.get('mematool', 'group_fullmember') in member.groups:
        member.groups.append(Config.get('mematool', 'group_fullmember'))
      elif not 'fullMember' in self.request.params and Config.get('mematool', 'group_fullmember') in member.groups:
        member.groups.remove(Config.get('mematool', 'group_fullmember'))

      if 'lockedMember' in self.request.params and not Config.get('mematool', 'group_lockedmember') in member.groups:
        member.groups.append(Config.get('mematool', 'group_lockedmember'))
      elif not 'lockedMember' in self.request.params and Config.get('mematool', 'group_lockedmember') in member.groups:
        member.groups.remove(Config.get('mematool', 'group_lockedmember'))

      self.mf.saveMember(member)

      self.session['flash'] = _('Member details successfully edited')
      self.session.save()

      raise HTTPRedirect('/members/editMember/?member_id={0}'.format(self.request.params['member_id']))

    except LookupError:
      print 'No such user !'

    # @TODO make much more noise !
    raise HTTPRedirect('/members/showAllMembers')

  @cherrypy.expose()
  @BaseController.needAdmin
  def showAllMembers(self, _filter='active'):
    c = TemplateContext()
    try:
      c.heading = _('All members')

      members = self.mf.getUsers(clear_credentials=True)
      c.members = []

      # make sure to clean out some vars
      for m in members:
        if _filter == 'active' and not m.lockedMember:
          c.members.append(m)
        elif _filter == 'former' and m.lockedMember:
          c.members.append(m)
        elif _filter == 'all':
          c.members.append(m)

      return self.render('/members/viewAll.mako', template_context=c)

    except LookupError as e:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      print 'Lookup error!'
      print e
      pass
    except NoResultFound:
      print 'No such sql user !'

    return 'ERROR 4x0'

  @cherrypy.expose()
  @BaseController.needAdmin
  def exportList(self, listType='plain'):
    c = TemplateContext()
    try:
      members = self.mf.getUsers()
      c.members = []

      # make sure to clean out some vars
      for m in members:
        m.sambaNTPassword = '******'
        m.userPassword = '******'

        if not m.lockedMember:
          c.members.append(m)

      if listType == 'RCSL':
        cherrypy.response.content_type = 'text/plain'
        return self.render('/members/exportRCSLCSV.mako', template_context=c)
      else:
        cherrypy.response.content_type = 'text/plain'
        return self.render('/members/exportCSV.mako', template_context=c)

    except LookupError as e:
      print 'Lookup error!'
      print e
      pass

    return 'ERROR 4x0'

  @cherrypy.expose()
  @BaseController.needAdmin
  def showActiveMembers(self):
    return self.showAllMembers(_filter='active')

  @cherrypy.expose()
  @BaseController.needAdmin
  def showFormerMembers(self):
    return self.showAllMembers(_filter='former')

  @cherrypy.expose()
  @BaseController.needAdmin
  def validateMember(self, member_id):
    try:
      member = self.mf.getUser(member_id)

      if member.validate:
        tm = self.db.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        member.givenName = tm.gn
        member.sn = tm.sn
        member.homePostalAddress = tm.homePostalAddress

        # @FIXME fix this nasty workaround
        if not tm.phone == '>>REMOVE<<':
          member.homePhone = tm.phone
        else:
          member.homePhone = ''

        member.mobile = tm.mobile
        member.mail = tm.mail
        member.xmppID = tm.xmppID

        self.mf.saveMember(member)
        self.db.delete(tm)
        self.db.commit()

        self.session['flash'] = _('Changes accepted')
        self.postValidationMail(member_id, member.mail, validated=True)
      else:
        self.session['flash'] = _('Nothing to validate!')

    except LookupError:
      self.session['flash'] = _('Member validation failed!')

    self.session.save()
    raise HTTPRedirect('/members/showAllMembers')

  @cherrypy.expose()
  @BaseController.needAdmin
  def rejectValidation(self, member_id):
    try:
      member = self.mf.getUser(member_id)

      if member.validate:
        tm = self.db.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        mail = tm.mail
        self.db.delete(tm)
        self.db.commit()

        self.session['flash'] = _('Changes rejected')
        self.postValidationMail(member_id, mail, validated=False)
      else:
        self.session['flash'] = _('Nothing to reject!')
        self.session['flash_class'] = 'error'

    except LookupError:
      self.session['flash'] = _('Failed to reject validation!')
      self.session['flash_class'] = 'error'

    self.session.save()
    raise HTTPRedirect('/members/showAllMembers')

  def postValidationMail(self, member_id, member_mail, validated=True):
    if validated:
      validation_string = 'validated'
    else:
      validation_string = 'rejected'

    # office e-mail
    body = 'Hi,\n'
    body += self.session['username'] + ' just ' + validation_string + ' the profile changes of the following member:\n'
    body += member_id + '\n\n'
    body += 'regards,\nMeMaTool'

    to = 'office@hackerspace.lu'
    subject = Config.get('mematool', 'name_prefix') + ' mematool - request for validation - ' + validation_string
    self.sendMail(to, subject, body)

    # user e-mail
    body = 'Hi,\n'
    body += 'The office has just ' + validation_string + ' your profile changes.\n'
    body += 'If you don\'t agree with this decision, please contact them for more information.\n\n'
    body += 'regards,\nMeMaTool on behalf of the office'

    self.sendMail(member_mail, subject, body)

  @cherrypy.expose()
  @BaseController.needAdmin
  def viewDiff(self, member_id):
    c = TemplateContext()

    try:
      member = self.mf.getUser(member_id)

      if member.validate:
        c.heading = _('View diff')
        c.member = member

        tmpmember = self.db.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        c.tmpmember = tmpmember

        return self.render('/members/viewDiff.mako', template_context=c)

    except LookupError:
      print 'No such user !'

    return 'ERROR 4x0'

  @cherrypy.expose()
  @BaseController.needAdmin
  def deleteUser(self, member_id):
    try:
      self.mf.deleteUser(member_id)

      aliases = self.mf.getMaildropList(member_id)
      errors = ''
      for dn, attr in aliases.items():
        if errors == '':
          errors = 'Could not auto-delete the following aliases:'

        m = re.match(r'^mail=([^,]+),', dn)
        if m:
          alias = m.group(1)
          url_ = url(controller='mails', action='editAlias', alias=alias)
          errors += '\n<br/><a href="{0}" target="_blank">{1}</a>'.format(url_, alias)

        if not errors == '':
          if not 'errors' in self.session:
            self.session['errors'] = []
          self.session['errors'].append(literal(errors))

      self.session['flash'] = _('User successfully deleted')
      self.session.save()
    except LookupError:
      self.session['flash'] = _('Failed to delete user')
      self.session.save()

    # @TODO make much more noise !
    raise HTTPRedirect('/members/showAllMembers')
