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
from pylons.i18n.translation import _

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member, TmpMember

log = logging.getLogger(__name__)

from mematool.lib.helpers import *

from sqlalchemy.orm.exc import NoResultFound
import re
from mematool.lib.syn2cat import regex
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat

from pylons.decorators.rest import restrict


class MembersController(BaseController):

  def __init__(self):
    super(MembersController, self).__init__()
    self.lmf = LdapModelFactory()

  @BaseController.needAdmin
  def __before__(self):
    super(MembersController, self).__before__()
    self._sidebar()

  def _sidebar(self):
    c.actions = list()
    c.actions.append({'name' : _('Show all members'), 'args' : {'controller' : 'members', 'action' : 'showAllMembers'}})
    c.actions.append({'name' : _('Add member'), 'args' : {'controller' : 'members', 'action' : 'addMember'}})
    c.actions.append({'name' : _('Active members'), 'args' : {'controller' : 'members', 'action' : 'showActiveMembers'}})
    c.actions.append({'name' : _('Former members'), 'args' : {'controller' : 'members', 'action' : 'showFormerMembers'}})
    c.actions.append({'name' : _('Groups'), 'args' : {'controller' : 'groups', 'action' : 'index'}})

  def index(self):
    return self.showAllMembers()

  @BaseController.needAdmin
  def addMember(self):
    c.heading = _('Add member')
    c.mode = 'add'
    c.groups = []

    return render('/members/editMember.mako')

  def editMember(self):
    if (not 'member_id' in request.params):
      redirect(url(controller='members', action='showAllMembers'))

    try:
      member = self.lmf.getUser(request.params['member_id'])

      c.heading = _('Edit member')
      c.mode = 'edit'

      c.member = member
      c.groups = self.lmf.getUserGroupList(request.params['member_id'])

      if member.fullMember:
        c.member.full_member = 'checked'
      if member.lockedMember:
        c.member.locked_member = 'checked'

      return render('/members/editMember.mako')

    except LookupError:
      print 'No such user !'

    return 'ERROR 4x0'

  def checkMember(f):
    def new_f(self):
      # @TODO request.params may contain multiple values per key... test & fix
      if (not 'member_id' in request.params):
        redirect(url(controller='members', action='showAllMembers'))
      else:
        formok = True
        errors = []

        try:
          ParamChecker.checkMode('mode', values=('add', 'edit'))
        except InvalidParameterFormat as ipf:
          formok = False
          errors.append(ipf.message)

        m = Member()

        for v in m.str_vars:
          setattr(m, v, request.params.get(v, ''))

        m.uid = request.params['member_id']

        try:
          m.check()
        except InvalidParameterFormat as ipf:
          formok = False
          errors += ipf.message

        if (request.params['mode'] == 'add') or\
          ('userPassword' in request.params and len(request.params['userPassword']) > 0):
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
            if (k == 'full_member' or k == 'locked_member') and request.params[k] == 'on':
              session['reqparams'][k] = 'checked'
            else:
              session['reqparams'][k] = request.params[k]

          session.save()

          if request.params['mode'] == 'add':
            redirect(url(controller='members', action='addMember'))
          else:
            redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))

      return f(self)
    return new_f

  @checkMember
  @restrict('POST')
  def doEditMember(self):
    try:
      if request.params['mode'] == 'edit':
        #member = Member(request.params['member_id'])
        member = self.lmf.getUser(request.params['member_id'])
      else:
        member = Member()
        member.uid = request.params['member_id']

      for v in member.str_vars:
        if v in request.params:
          setattr(member, v, request.params.get(v).lstrip(' ').rstrip(' '))

      # @TODO review: for now we don't allow custom GIDs
      #member.gidNumber = request.params['gidNumber']
      member.gidNumber = '100'
      member.cn = member.givenName + ' ' + member.sn
      member.homeDirectory = '/home/' + request.params['member_id']

      if 'userPassword' in request.params and 'userPassword2' in request.params and request.params['userPassword'] != '' and request.params['userPassword'] == request.params['userPassword2']:
        member.setPassword(request.params['userPassword'])

      if 'full_member' in request.params:
        member.fullMember = True
      else:
        member.fullMember = False

      if 'locked_member' in request.params:
        member.lockedMember = True
      else:
        member.lockedMember = False

      if 'spaceKey' in request.params:
        member.spaceKey = True
      else:
        member.spaceKey = False

      if 'npoMember' in request.params:
        member.npoMember = True
      else:
        member.npoMember = False

      member.nationality = member.nationality.upper()

      if request.params['mode'] == 'edit':
        self.lmf.saveMember(member)
      else:
        self.lmf.saveMember(member)

      session['flash'] = _('Member details successfully edited')
      session.save()

      redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))

    except LookupError:
      print 'No such user !'

    # @TODO make much more noise !
    redirect(url(controller='members', action='showAllMembers'))

  def showAllMembers(self, _filter='active'):
    try:
      c.heading = _('All members')

      members = self.lmf.getUsers()
      c.members = []

      # make sure to clean out some vars
      for m in members:
        if m.sambaNTPassword != '':
          m.sambaNTPassword = '******'
        if m.userPassword != '':
          m.userPassword = '******'

        if _filter == 'active' and not m.lockedMember:
          c.members.append(m)
        elif _filter == 'former' and m.lockedMember:
          c.members.append(m)
        elif _filter == 'all':
          c.members.append(m)

      return render('/members/viewAll.mako')

    except LookupError as e:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      print 'Lookup error!'
      print e
      pass
    except NoResultFound:
      print 'No such sql user !'

    return 'ERROR 4x0'

  def exportList(self):
    try:
      members = self.lmf.getUsers()
      c.members = []

      # make sure to clean out some vars
      for m in members:
        if m.sambaNTPassword != '':
          m.sambaNTPassword = '******'
        if m.userPassword != '':
          m.userPassword = '******'

        if not m.lockedMember:
          c.members.append(m)

      if 'listType' in request.params and request.params['listType'] == 'RCSL':
        response.content_type = 'text/plain'
        return render('/members/exportRCSLCSV.mako')
      else:
        response.content_type = 'text/plain'
        return render('/members/exportCSV.mako')

    except LookupError as e:
      print 'Lookup error!'
      print e
      pass

    return 'ERROR 4x0'

  def showActiveMembers(self):
    return self.showAllMembers(_filter='active')

  def showFormerMembers(self):
    return self.showAllMembers(_filter='former')

  def validateMember(self):
    if (not 'member_id' in request.params):
      redirect(url(controller='members', action='showAllMembers'))

    try:
      member = self.lmf.getUser(request.params['member_id'])

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

        self.lmf.saveMember(member)
        Session.delete(tm)
        Session.commit()

        self.postValidationMail(request.params['member_id'], member.mail, validated=True)
      else:
        session['flash'] = _('Nothing to validate!')

    except LookupError:
      session['flash'] = _('Member validation failed!')

    session.save()
    redirect(url(controller='members', action='showAllMembers'))

  def rejectValidation(self):
    if (not 'member_id' in request.params):
      redirect(url(controller='members', action='showAllMembers'))

    try:
      member = self.lmf.getUser(request.params['member_id'])

      if member.validate:
        tm = Session.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        mail = tm.mail
        Session.delete(tm)
        Session.commit()

        self.postValidationMail(request.params['member_id'], mail, validated=False)
      else:
        session['flash'] = _('Nothing to reject!')

    except LookupError:
      session['flash'] = _('Failed to reject validation!')

    session.save()
    redirect(url(controller='members', action='showAllMembers'))

  def postValidationMail(self, member_id, member_mail, validated=True):
    if validated:
      validation_string = 'validated'
    else:
      validation_string = 'rejected'

    # office e-mail
    body = 'Hi,\n'
    body += session['identity'] + ' just ' + validation_string + ' the profile changes of the following member:\n'
    body += member_id + '\n\n'
    body += 'regards,\nMeMaTool'

    to = 'office@hackerspace.lu'
    subject = config.get('mematool.name_prefix') + ' mematool - request for validation - ' + validation_string
    self.sendMail(to, subject, body)

    # user e-mail
    body = 'Hi,\n'
    body += 'The office has just ' + validation_string + ' your profile changes.\n'
    body += 'If you don\'t agree with this decision, please contact them for more information.\n\n'
    body += 'regards,\nMeMaTool on behalf of the office'

    self.sendMail(member_mail, subject, body)

  def viewDiff(self):
    if (not 'member_id' in request.params):
      redirect(url(controller='members', action='showAllMembers'))

    try:
      member = self.lmf.getUser(request.params['member_id'])

      if member.validate:
        c.heading = _('View diff')
        c.member = member

        tmpmember = Session.query(TmpMember).filter(TmpMember.id == member.uidNumber).first()
        c.tmpmember = tmpmember

        return render('/members/viewDiff.mako')

    except LookupError:
      print 'No such user !'

    return 'ERROR 4x0'

  @BaseController.needAdmin
  def deleteUser(self):
    try:
      member_id = request.params.get('member_id')
      self.lmf.deleteUser(member_id)

      aliases = self.lmf.getMaildropList(member_id)
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
          if not 'errors' in session:
            session['errors'] = []
          session['errors'].append(literal(errors))

      session['flash'] = _('User successfully deleted')
      session.save()
    except LookupError:
      session['flash'] = _('Failed to delete user')
      session.save()


    # @TODO make much more noise !
    redirect(url(controller='members', action='showAllMembers'))
