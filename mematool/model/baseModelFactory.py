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

import cherrypy
from sqlalchemy.orm.exc import NoResultFound
from mematool.model.dbmodel import Group

log = logging.getLogger(__name__)


class BaseModelFactory(object):
  @property
  def db(self):
    return cherrypy.request.db

  def authenticate(self, username, password):
    raise NotImplemented()

  def getUser(self, uid, clear_credentials=False):
    raise NotImplemented()

  def getUserList(self):
    raise NotImplemented()

  def getActiveMemberList(self):
    '''Get a list of members not belonging to the locked-members group'''
    users = []

    for u in self.getUserList():
      if not self.isUserInGroup(u, Config.get('mematool', 'group_lockedmember')):
        users.append(u)

    return users

  def getUsers(self, clear_credentials=False):
    '''Return a list of all user objects'''
    users = []

    for uid in self.getUserList():
      users.append(self.getUser(uid))

    return users

  def getUserGroupList(self, uid):
    raise NotImplemented()

  def isUserInGroup(self, uid, gid):
    '''Is the specified user in the requested group ?'''
    if uid in self.getGroupMembers(gid):
      return True

    return False

  def getHighestUidNumber(self):
    raise NotImplemented()

  def getUidNumberFromUid(self, uid):
    raise NotImplemented()

  def saveMember(self, member, is_admin=True):
    '''Add or update a member object in LDAP'''
    if member.uidNumber and member.uidNumber > 0:
      '''Existing member -> update'''
      self._updateMember(member, is_admin)
    else:
      self._addMember(member)

  def _updateMember(self, member, is_admin=True):
    raise NotImplemented()

  def _addMember(self, member):
    raise NotImplemented()

  def changeUserGroup(self, uid, group, status):
    raise NotImplemented()

  def getGroup(self, gid):
    raise NotImplemented()

  def getGroupList(self):
    raise NotImplemented()

  def getManagedGroupList(self):
    ret = []

    try:
      ret = self.db.query(Group).order_by(Group.gid).all()
    except:
      pass

    return ret

  def getGroupMembers(self, group):
    raise NotImplemented()

  def addGroup(self, gid):
    try:
      sql_group = self.db.query(Group).filter(Group.gid == gid).one()
      return True
    except LookupError:
      print 'Fatal error...'
      return False
    except NoResultFound:
      '''SQL entry does not exist, create it'''
      try:
        g = Group()
        g.gid = gid
        cherrypy.request.db.add(g)
        cherrypy.request.db.commit()
        return True
      except:
        return False

  def unmanageGroup(self, gid):
    try:
      g = self.db.query(Group).filter(Group.gid == gid).one()
      cherrypy.request.db.delete(g)
      cherrypy.request.db.commit()

      return True
    except Exception as e:
      ''' Don't care '''
      pass

    return False

  def deleteGroup(self, gid):
    try:
      sql_group = self.db.query(Group).filter(Group.gid == gid).one()
      cherrypy.request.db.delete(sql_group)
      cherrypy.request.db.commit()
      return True
    except:
      '''Don't care'''
      pass

    return False

  def getHighestGidNumber(self):
    raise NotImplemented()

  def addDomain(self, domain):
    raise NotImplemented()

  def deleteDomain(self, domain):
    raise NotImplemented()

  def getDomain(self, domain):
    raise NotImplemented()

  def getDomainList(self):
    raise NotImplemented()

  def getDomains(self):
    '''Return a list of all domain objects'''
    domains = []

    for domain in self.getDomainList():
      domains.append(self.getDomain(domain))

    return domains

  def getAlias(self, alias):
    raise NotImplemented()

  def getAliasList(self, domain):
    raise NotImplemented()

  def getAliases(self, domain):
    '''Return a list of all alias objects'''
    aliases = []

    for alias in self.getAliasList(domain):
      aliases.append(self.getAlias(alias))

    return aliases

  def deleteAlias(self, alias):
    raise NotImplemented()
