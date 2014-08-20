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

import logging

from mematool.model.baseModelFactory import BaseModelFactory
from mematool.model.dbmodel import Group
from mematool.model.ldapmodel import Member, Domain, Alias
from mematool import Config
from mematool.helpers.exceptions import EntryExists


log = logging.getLogger(__name__)


class StaticModelFactory(BaseModelFactory):
  def __init__(self):
    super(StaticModelFactory, self).__init__()

  def authenticate(self, username, password):
    return True

  def close(self):
    pass

  def getUser(self, uid, clear_credentials=False):
    m = Member()

    for k in m.str_vars:
        v = 'test'

        if k == 'sambaSID':
          v = None

        m.set_property(k, v)

    if clear_credentials:
      m.sambaNTPassword = '******'
      m.userPassword = '******'

    m.groups = self.getUserGroupList(uid)

    return m

  def getUserList(self):
    users = [1000, 1001]

    return users

  def getUserGroupList(self, uid):
    '''Get a list of groups a user is a member of'''
    groups = ['test_group', 'group1', 'grp_full_member']

    return groups

  def getHighestUidNumber(self):
    '''Get the highest used uid-number
    this is used when adding a new user'''
    uidNumber = 1001

    uidNumber += 1

    return str(uidNumber)

  def getUidNumberFromUid(self, uid):
    '''Get a UID-number based on its UID'''

    if not uid in ['test1', 'test2']:
      raise LookupError('No such user !')

    return 1000

  def prepareVolatileAttribute(self, member, oldmember=None, attribute=None, encoding='utf-8'):
    '''Checks if an attribute is present in the member object and
    whether it should be updated or else deleted.
    While doing that it converts the attribute value to the specified
    encoding, which by default is UTF-8
    Returns None if the attribute it not present or nothing should be
    changed'''
    retVal = None

    if hasattr(member, attribute):
      a = getattr(member, attribute)

    if isinstance(a, bool) or (a and not a is None and a != ''):
      ''' be careful with bool attributes '''
      if isinstance(a, bool):
        a = str(a).upper()
      else:
        if not encoding is None:
          a = str(a.encode(encoding, 'ignore'))

      if oldmember and hasattr(oldmember, attribute) and not getattr(oldmember, attribute) is None and not getattr(oldmember, attribute) == '':
        # @FIXME UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal
        #   if not a == getattr(oldmember, attribute):
        if not a == getattr(oldmember, attribute):
          retVal = (ldap.MOD_REPLACE, attribute, a)
      else:
        if not oldmember is None:
          retVal = (ldap.MOD_ADD, attribute, a)
        else:
          retVal = (attribute, [a])
    else:
      if oldmember and hasattr(oldmember, attribute) and not getattr(oldmember, attribute) is None and not getattr(oldmember, attribute) == '':
        retVal = (ldap.MOD_DELETE, attribute, None)

    return retVal

  def _updateMember(self, member, is_admin=True):
    return True

  def _addMember(self, member):
    return True

  def deleteUser(self, uid):
    return True

  def changeUserGroup(self, uid, group, status):
    return True

  def updateAvatar(self, member, b64_jpg):
    return True

  def getGroup(self, gid):
    ''' Get a specific group'''
    g = Group()
    g.users = ['test1', 'test2']
    g.gid = 1000

    return g

  def getGroupList(self):
    '''Get a list of all groups'''
    groups = ['test_group']

    return groups

  def getGroupMembers(self, group):
    '''Get all members of a specific group'''
    members = ['test1', 'test2']

    return members

  def addGroup(self, gid):
    return True

  def deleteGroup(self, gid):
    return True

  def getHighestGidNumber(self):
    '''Get the highest used gid-number
    this is used when adding a new group'''
    gidNumber = 1000

    gidNumber += 1

    return str(gidNumber)

  def addDomain(self, domain):
    return True

  def deleteDomain(self, domain):
    return True

  def getDomain(self, domain):
    filter_ = '(objectClass=mailDomain)'
    attrs = ['*']
    basedn = 'dc=' + str(domain) + ',' + str(Config.get('ldap', 'basedn'))

    result = self.ldapcon.search_s(basedn, ldap.SCOPE_BASE, filter_, attrs)

    if not result:
      raise LookupError('No such domain !')

    d = Domain()

    for dn, attr in result:
      for k, v in attr.iteritems():
        if 'objectClass' in k:
          # @TODO ignore for now
          continue

        # @TODO handle multiple results
        v = v[0]

        setattr(d, k, v)

    return d

  def getDomainList(self):
    result = self.ldapcon.search_s(Config.get('ldap', 'basedn'), ldap.SCOPE_SUBTREE, Config.get('ldap', 'domain_filter'), [Config.get('ldap', 'domain_filter_attrs')])

    domains = []

    for dn, attr in result:
      for key, value in attr.iteritems():
        if len(value) == 1:
          domains.append(value[0])
        else:
          for i in value:
            domains.append(i)

    return domains

  def getAlias(self, alias):
    filter_ = '(&(objectClass=mailAlias)(mail=' + str(alias) + '))'
    attrs = ['*']
    basedn = str(Config.get('ldap', 'basedn'))
    result = self.ldapcon.search_s(basedn, ldap.SCOPE_SUBTREE, filter_, attrs)

    if not result:
      raise LookupError('No such alias !')

    a = Alias()
    a.dn_mail = alias

    for dn, attr in result:
      for k, v in attr.iteritems():
        if 'objectClass' in k:
          # @TODO ignore for now
          continue
        elif k == 'mail':
          if len(v) == 1:
            a.mail.append(v[0])
          else:
            for i in v:
              a.mail.append(i)

          continue
        elif k == 'maildrop':
          if len(v) == 1:
            a.maildrop.append(v[0])
          else:
            for i in v:
              a.maildrop.append(i)

          continue
        else:
          # @TODO handle multiple results
          v = v[0]

          setattr(a, k, v)

    return a

  def getAliasList(self, domain):
    filter_ = 'objectClass=mailAlias'
    attrs = ['']
    basedn = 'dc=' + str(domain) + ',' + str(Config.get('ldap', 'basedn'))
    result = self.ldapcon.search_s(basedn, ldap.SCOPE_SUBTREE, filter_, attrs)

    aliases = []

    for dn, attr in result:
      dn_split = dn.split(',')
      a = dn_split[0].split('=')[1]

      aliases.append(a)

    return aliases

  def getMaildropList(self, uid):
    '''This returns all aliases which have as maildrop the specified uid'''
    filter_ = '(&(objectClass=mailAlias)(maildrop={0}))'.format(uid)
    attrs = ['maildrop']
    basedn = str(Config.get('ldap', 'basedn'))
    result = self.ldapcon.search_s(basedn, ldap.SCOPE_SUBTREE, filter_, attrs)

    aliases = {}

    if not result:
      return aliases

    for dn, attr in result:
      if not dn in aliases:
        aliases[dn] = []

      for a in attr['maildrop']:
        aliases[dn].append(a)

    return aliases

  def addAlias(self, alias):
    try:
      oldalias = self.getAlias(alias.dn_mail)

      raise EntryExists('Alias already exists!')
    except:
      mod_attrs = []
      mod_attrs.append(('objectClass', ['mailAlias']))

      mail = []
      for m in alias.mail:
        mail.append(str(m.encode('utf-8', 'ignore')))

      if len(mail) > 0:
        mod_attrs.append(('mail', mail))

      maildrop = []
      for m in alias.maildrop:
        maildrop.append(str(m.encode('utf-8', 'ignore')))

      if len(maildrop) > 0:
        mod_attrs.append(('maildrop', maildrop))

      while None in mod_attrs:
        mod_attrs.remove(None)

      dn = 'mail=' + alias.dn_mail + ',dc=' + alias.domain + ',' + Config.get('ldap', 'basedn')
      dn = dn.encode('ascii', 'ignore')

      try:
        result = self.ldapcon.add_s(dn, mod_attrs)
      except ldap.ALREADY_EXISTS:
        raise EntryExists('Alias already exists!')

      if result is None:
        return False

      return True

    return False

  def updateAlias(self, alias):
    # @FIXME https://github.com/sim0nx/mematool/issues/1
    oldalias = self.getAlias(alias.dn_mail)
    mod_attrs = []

    for m in alias.mail:
      if m == alias.dn_mail:
        continue

      found = False
      for n in oldalias.mail:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_ADD, 'mail', m.encode('ascii', 'ignore')))

    for m in oldalias.mail:
      if m == oldalias.dn_mail:
        continue

      found = False
      for n in alias.mail:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_DELETE, 'mail', m.encode('ascii', 'ignore')))

    for m in alias.maildrop:
      if m == alias.dn_mail:
        continue

      found = False
      for n in oldalias.maildrop:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_ADD, 'maildrop', m.encode('ascii', 'ignore')))

    for m in oldalias.maildrop:
      if m == oldalias.dn_mail:
        continue

      found = False
      for n in alias.maildrop:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_DELETE, 'maildrop', m.encode('ascii', 'ignore')))

    while None in mod_attrs:
      mod_attrs.remove(None)

    # nothing to do
    if len(mod_attrs) == 0:
      return True

    dn = alias.getDN(Config.get('ldap', 'basedn')).encode('ascii', 'ignore')

    result = self.ldapcon.modify_s(dn, mod_attrs)

    if result is None:
      return False

    return True

  def deleteMaildrop(self, alias, uid):
    mod_attrs = []
    mod_attrs.append((ldap.MOD_DELETE, 'maildrop', uid.encode('ascii', 'ignore')))

    result = self.ldapcon.modify_s(alias, mod_attrs)

    if result is None:
      return False

    return True

  def deleteAlias(self, alias):
    '''Completely remove an alias'''

    a = self.getAlias(alias)
    dn = a.getDN(Config.get('ldap', 'basedn')).encode('ascii', 'ignore')
    retVal = self.ldapcon.delete_s(dn)

    if not retVal is None:
      return True

    return False
