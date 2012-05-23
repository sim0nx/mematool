#
# MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
# This file is part of MeMaTool.
#
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.


import logging

from pylons import config
from pylons.i18n.translation import _

#from mematool.lib.base import Session
#from sqlalchemy.orm.exc import NoResultFound
from mematool.model.baseModelFactory import BaseModelFactory
from mematool.model import Member
from mematool.model import Group
from mematool.model import Domain
from mematool.model import Alias
 
log = logging.getLogger(__name__)

from mematool.lib.syn2cat.ldapConnector import LdapConnector
import ldap
import re


class LdapModelFactory(BaseModelFactory):
  def __init__(self, cnf=None):
    super(LdapModelFactory, self).__init__()
    self.ldapcon = None

    if cnf is not None:
      self.cnf = cnf
    else:
      self.cnf = config

    if 'ldapcon' in self.cnf['mematool'] and not self.cnf['mematool']['ldapcon'] is None:
      self.ldapcon = self.cnf['mematool']['ldapcon']
    else:
      self.cnf['mematool']['ldapcon'] = LdapConnector(cnf=cnf).getLdapConnection()
      self.ldapcon = self.cnf['mematool']['ldapcon']

  def close(self):
    self.ldapcon = None

  def getUser(self, uid):
    filter_ = '(uid=' + uid + ')'
    attrs = ['*']
    basedn = 'uid=' + str(uid) + ',' + str(self.cnf.get('ldap.basedn_users'))

    result = self.ldapcon.search_s( basedn, ldap.SCOPE_SUBTREE, filter_, attrs )

    if not result:
      raise LookupError('No such user !')

    m = Member()

    for dn, attr in result:
      for k, v in attr.iteritems():
        if 'objectClass' in k:
          # @TODO ignore for now
          continue

        # @TODO handle multiple results
        v = v[0]

        if k == 'sambaSID' and v == '':
          v = None
        elif k == 'spaceKey' or k == 'npoMember':
          if v.lower() == 'true':
            v = True
          else:
            v = False

        setattr(m, k, v)

    m.groups = self.getUserGroupList(uid)

    # @TODO make this generic
    if 'syn2cat_full_member' in m.groups:
      m.fullMember = True
    if 'syn2cat_locked_member' in m.groups:
      m.lockedMember = True

    return m

  def getUserList(self):
    '''Get a list of all users belonging to the group "users" (gid-number = 100)
    and having a uid-number >= 1000 and < 65000'''
    filter = '(&(uid=*)(gidNumber=100))'
    attrs = ['uid', 'uidNumber']
    users = []

    result = self.ldapcon.search_s( self.cnf.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

    for dn, attr in result:
      if int(attr['uidNumber'][0]) >= 1000 and int(attr['uidNumber'][0]) < 65000:
        users.append( attr['uid'][0] )

    users.sort()

    return users

  def getActiveMemberList(self):
    users = self.getUserList()
    ausers = []

    for u in users:
      if not self.isUserInGroup(u, 'syn2cat_locked_member'):
        ausers.append(u)

    return ausers
        

  def getUserGroupList(self, uid):
    '''Get a list of groups a user is a member of'''
    filter = '(memberUid=' + uid + ')'
    attrs = ['cn']
    groups = []

    result = self.ldapcon.search_s( self.cnf.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )

    for dn, attr in result:
      for key, value in attr.iteritems():
        if len(value) == 1:
          groups.append(value[0])
        else:
          for i in value:
            groups.append(i)

    return groups

  def getHighestUidNumber(self):
    '''Get the highest used uid-number
    this is used when adding a new user'''
    result = self.ldapcon.search_s( self.cnf.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, self.cnf.get('ldap.uid_filter'), [self.cnf.get('ldap.uid_filter_attrs')] )

    uidNumber = -1

    for dn, attr in result:
      for key, value in attr.iteritems():
        if int(value[0]) > uidNumber and int(value[0]) < 65000:
          uidNumber = int(value[0])

    uidNumber += 1

    return str(uidNumber)

  def getUidNumberFromUid(self, uid):
    '''Get a UID-number based on its UID'''
    filter = '(uid=' + uid + ')'
    attrs = ['uidNumber']

    result = self.ldapcon.search_s( self.cnf.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )
    
    if not result:
      raise LookupError('No such user !')

    for dn, attr in result:
      uidNumber = attr['uidNumber'][0]

    return uidNumber

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
        a = str(a.encode(encoding, 'ignore'))

      if oldmember and hasattr(oldmember, attribute) and not getattr(oldmember, attribute) is None and not getattr(oldmember, attribute) == '':
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
    mod_attrs = []
    om = self.getUser(member.uid)

    if is_admin:
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'cn'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'sn'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'givenName'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'homePostalAddress'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'homePhone'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'mobile'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'mail'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'gidNumber'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'loginShell'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'homeDirectory'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'birthDate'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'arrivalDate'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'leavingDate'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'sshPublicKey'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'pgpKey'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'iButtonUID'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'conventionSigner'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'xmppID'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'spaceKey'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'npoMember'))
      mod_attrs.append(self.prepareVolatileAttribute(member, om, 'nationality'))

    if member.userPassword and member.userPassword != '':
      mod_attrs.append((ldap.MOD_REPLACE, 'userPassword', str(member.userPassword)))
      if member.sambaNTPassword and member.sambaNTPassword != '':
        mod_attrs.append((ldap.MOD_REPLACE, 'sambaNTPassword', str(member.sambaNTPassword)))

    while None in mod_attrs:
      mod_attrs.remove(None)

    result = self.ldapcon.modify_s('uid=' + member.uid + ',' + self.cnf.get('ldap.basedn_users'), mod_attrs)

    self.changeUserGroup(member.uid, 'syn2cat_full_member', member.fullMember)
    self.changeUserGroup(member.uid, 'syn2cat_locked_member', member.lockedMember)

    return result

  def _addMember(self, member):
    '''Add a new user'''
    member.uidNumber = self.getHighestUidNumber()
    member.generateUserSID()

    mod_attrs = []

    mod_attrs.append(('objectclass', ['posixAccount', 'organizationalPerson', 'inetOrgPerson', 'shadowAccount', 'top', 'samsePerson', 'sambaSamAccount', 'ldapPublicKey', 'syn2catPerson']))
    mod_attrs.append(('ou', ['People']))

    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'uid'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'cn'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'sn'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'givenName'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'homePostalAddress'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'homePhone'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'mobile'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'mail'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'gidNumber'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'loginShell'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'homeDirectory'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'birthDate'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'arrivalDate'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'leavingDate'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'sshPublicKey'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'pgpKey'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'iButtonUID'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'conventionSigner'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'xmppID'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'spaceKey'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'npoMember'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'nationality'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'userPassword'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'uidNumber'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'sambaSID'))
    mod_attrs.append(self.prepareVolatileAttribute(member, None, 'sambaNTPassword'))

    while None in mod_attrs:
      mod_attrs.remove(None)

    dn = 'uid=' + member.uid + ',' + self.cnf.get('ldap.basedn_users')
    dn = dn.encode('ascii','ignore')
    result = self.ldapcon.add_s( dn, mod_attrs)

    self.changeUserGroup(member.uid, 'syn2cat_full_member', member.fullMember)
    self.changeUserGroup(member.uid, 'syn2cat_locked_member', member.lockedMember)

    return result

  def changeUserGroup(self, uid, group, status):
    '''Change user/group membership'''
    '''@TODO check and fwd return value'''
    mod_attrs = []
    result = ''
    m = self.getUser(uid)

    if status and not group in m.groups:
      mod_attrs = [ (ldap.MOD_ADD, 'memberUid', uid.encode('ascii','ignore')) ]
    elif not status and group in m.groups:
      mod_attrs = [ (ldap.MOD_DELETE, 'memberUid', uid.encode('ascii','ignore')) ]

    if len(mod_attrs) == 1:
      try:
        result = self.ldapcon.modify_s('cn=' + group.encode('ascii','ignore') + ',' + self.cnf.get('ldap.basedn_groups'), mod_attrs)
      except (ldap.TYPE_OR_VALUE_EXISTS, ldap.NO_SUCH_ATTRIBUTE):
        pass
      except:
        print sys.exc_info()[0]
        pass

    return result

  def getGroup(self, gid):
    ''' Get a specific group'''
    filter = '(cn=' + gid + ')'
    attrs = ['*']

    result = self.ldapcon.search_s( self.cnf.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )

    if not result:
      raise LookupError('No such group !')

    g = Group()
    g.users = []
    for dn, attr in result:
      for k, v in attr.iteritems():
        if 'cn' in k:
          k = 'gid'

        if 'memberUid' in k:
          for m in v:
            g.users.append(m)
        else:
          v = v[0]
          setattr(g, k, v)

    return g

  def getGroupList(self):
    '''Get a list of all groups'''
    filter = '(cn=*)'
    attrs = ['cn', 'gidNumber']
    
    result = self.ldapcon.search_s( self.cnf.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )
    groups = []
    
    for dn, attr in result:
      groups.append( attr['cn'][0] )

    return groups

  def getGroupMembers(self, group):
    '''Get all members of a specific group'''
    filter = '(cn=' + group + ')'
    attrs = ['memberUid']

    result = self.ldapcon.search_s(self.cnf.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs)

    if not result:
      raise LookupError('No such group !')

    members = []

    for dn, attr in result:
      for key, value in attr.iteritems():
        if len(value) == 1:
          members.append(value[0])
        else:
          for i in value:
            members.append(i)

    return members

  def addGroup(self, gid):
    '''Add a new group'''
    if super(LdapModelFactory, self).addGroup(gid):
      gl = self.getGroupList()

      if not gid in gl:
        g = Group()
        g.gid = gid
        g.gidNumber = self.getHighestGidNumber()
        mod_attrs = []

        mod_attrs.append(('objectClass', ['top', 'posixGroup']))

        mod_attrs.append(self.prepareVolatileAttribute(g, None, 'cn'))
        mod_attrs.append(self.prepareVolatileAttribute(g, None, 'gidNumber'))

        while None in mod_attrs:
          mod_attrs.remove(None)

        dn = 'cn=' + gid + ',' + self.cnf.get('ldap.basedn_groups')
        dn = dn.encode('ascii','ignore')
        result = self.ldapcon.add_s( dn, mod_attrs)

        if result is None:
          return False

      return True

    return False

  def deleteGroup(self, gid):
    '''Completely remove a group'''
    dn = 'cn=' + gid + ',' + self.cnf.get('ldap.basedn_groups')
    dn = dn.encode('ascii','ignore')
    retVal = self.ldapcon.delete_s(dn)

    if not retVal is None and super(LdapModelFactory, self).deleteGroup(gid):
      return True

    return False

  def getHighestGidNumber(self):
    '''Get the highest used gid-number
    this is used when adding a new group'''
    result = self.ldapcon.search_s(self.cnf.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, self.cnf.get('ldap.gid_filter'), [self.cnf.get('ldap.gid_filter_attrs')])

    gidNumber = -1

    for dn, attr in result:
      for key, value in attr.iteritems():
        if int(value[0]) > gidNumber and int(value[0]) < 65000:
          gidNumber = int(value[0])

    gidNumber += 1

    return str(gidNumber)

  def addDomain(self, domain):
    '''Add a new domain'''
    dl = self.getDomainList()

    if not domain in dl:
      d = Domain()
      d.dc = domain
      mod_attrs = []

      mod_attrs.append(('objectClass', ['top', 'domain', 'mailDomain']))
      mod_attrs.append(self.prepareVolatileAttribute(d, None, 'dc'))

      while None in mod_attrs:
        mod_attrs.remove(None)

      dn = 'dc=' + domain + ',' + self.cnf.get('ldap.basedn')
      dn = dn.encode('ascii','ignore')
      result = self.ldapcon.add_s( dn, mod_attrs)

      if result is None:
        return False

      return True

    return False

  def deleteDomain(self, domain):
    '''Completely remove a domain'''
    dl = self.getDomainList()

    if domain in dl:
      dn = 'dc=' + domain + ',' + self.cnf.get('ldap.basedn')
      dn = dn.encode('ascii','ignore')
      retVal = self.ldapcon.delete_s(dn)

      if not retVal is None:
        return True
    else:
      raise LookupError('No such domain!')

    return False

  def getDomain(self, domain):
    filter_ = '(objectClass=mailDomain)'
    attrs = ['*']
    basedn = 'dc=' + str(domain) + ',' + str(self.cnf.get('ldap.basedn'))

    result = self.ldapcon.search_s( basedn, ldap.SCOPE_BASE, filter_, attrs )

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
    result = self.ldapcon.search_s(self.cnf.get('ldap.basedn'), ldap.SCOPE_SUBTREE, self.cnf.get('ldap.domain_filter'), [self.cnf.get('ldap.domain_filter_attrs')])

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
    basedn = str(self.cnf.get('ldap.basedn'))
    result = self.ldapcon.search_s( basedn, ldap.SCOPE_SUBTREE, filter_, attrs )

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
    basedn = 'dc=' + str(domain) + ',' + str(self.cnf.get('ldap.basedn'))
    result = self.ldapcon.search_s(basedn, ldap.SCOPE_SUBTREE, filter_, attrs)

    aliases = []

    for dn, attr in result:
      dn_split = dn.split(',')
      a = dn_split[0].split('=')[1]
      
      aliases.append(a)

    return aliases

  def addAlias(self, alias):
    try:
      oldalias = self.getAlias(alias.dn_mail)

      raise Exception('Alias already exists!')
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

      dn = 'mail=' + alias.dn_mail + ',dc=' + alias.domain + ',' + self.cnf.get('ldap.basedn')
      dn = dn.encode('ascii','ignore')

      result = self.ldapcon.add_s( dn, mod_attrs)

      if result is None:
        return False

      return True

    return False

  def updateAlias(self, alias):
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
        mod_attrs.append((ldap.MOD_ADD, 'mail', m.encode('ascii','ignore')))

    for m in oldalias.mail:
      if m == oldalias.dn_mail:
        continue

      found = False
      for n in alias.mail:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_DELETE, 'mail', m.encode('ascii','ignore')))

    for m in alias.maildrop:
      if m == alias.dn_mail:
        continue

      found = False
      for n in oldalias.maildrop:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_ADD, 'maildrop', m.encode('ascii','ignore')))

    for m in oldalias.maildrop:
      if m == oldalias.dn_mail:
        continue

      found = False
      for n in alias.maildrop:
        if m == n:
          found = True
          break

      if not found:
        mod_attrs.append((ldap.MOD_DELETE, 'maildrop', m.encode('ascii','ignore')))


    while None in mod_attrs:
      mod_attrs.remove(None)


    # nothing to do
    if len(mod_attrs) == 0:
      return True

    dn = alias.getDN(self.cnf.get('ldap.basedn')).encode('ascii','ignore')
    result = self.ldapcon.modify_s( dn, mod_attrs)

    if result is None:
      return False

    return True

  def deleteAlias(self, alias):
    '''Completely remove a alias'''

    a = self.getAlias(alias)
    dn =  a.getDN(self.cnf.get('ldap.basedn')).encode('ascii','ignore')
    retVal = self.ldapcon.delete_s(dn)

    if not retVal is None:
      return True

    return False



