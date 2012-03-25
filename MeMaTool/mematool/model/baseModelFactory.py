#
#	MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
#	This file is part of MeMaTool.
#
#
#	MeMaTool is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Foobar is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.


import logging

from pylons import config

from mematool.lib.base import Session
from sqlalchemy.orm.exc import NoResultFound
from mematool.model import Member
from mematool.model import Group

log = logging.getLogger(__name__)

import gettext
_ = gettext.gettext



class BaseModelFactory(object):
	def __init__(self):
		pass

	def getUser(self, uid):
		pass

	def getUserList(self):
		pass

	def getUsers(self):
		'''Return a list of all member objects'''
		ul = self.getUserList()
		users = []

		for v in ul:
			users.append(self.getUser(v))

		return users

	def getUserGroupList(self, uid):
		pass

	def isUserInGroup(self, uid, gid):
		'''Is the specified user in the requested group ?'''
		if uid in self.getGroupMembers(gid):
			return True

		return False

	def getHighestUidNumber(self):
		pass

	def getUidNumberFromUid(self, uid):
		pass

	def saveMember(self, member):
		'''Add or update a member object in LDAP'''
		if member.uidNumber and member.uidNumber > 0:
			'''Existing member -> update'''
			self._updateMember(member)
		else:
			self._addMember(member)

	def _updateMember(self, member):
		pass

	def _addMember(self, member):
		pass

	def changeUserGroup(self, uid, group, status):
		pass

	def getGroup(self, gid):
		pass

	def getGroupList(self):
		pass

	def getManagedGroupList(self):
		try:
			g = Session.query(Group).order_by(Group.gid).all()

			return g
		except:
			pass

		return []


	def getGroupMembers(self, group):
		pass

	def addGroup(self, gid):
		try:
			sql_group = Session.query(Group).filter(Group.gid == gid).one()
			return True
		except LookupError:
			print 'Fatal error...'
			return False
		except NoResultFound:
			'''SQL entry does not exist, create it'''
			try:
				g = Group()
				g.gid = gid
				Session.add(g)
				Session.commit()
				return True
			except:
				return False

	def unmanageGroup(self, gid):
		try:
			g = Session.query(Group).filter(Group.gid == gid).one()
			Session.delete(g)
			Session.commit()

			return True
		except Exception as e:
			''' Don't care '''
			pass

		return False

	def deleteGroup(self, gid):
		try:
			sql_group = Session.query(Group).filter(Group.gid == gid).one()
			Session.delete(sql_group)
			Session.commit()
			return True
		except:
			'''Don't care'''
			pass

		return False

	def getHighestGidNumber(self):
		pass

	def addDomain(self, domain):
		pass

	def deleteDomain(self, domain):
		pass

	def getDomain(self, domain):
		pass

	def getDomainList(self):
		pass

	def getDomains(self):
		'''Return a list of all domain objects'''
		dl = self.getDomainList()
		domains = []

		for v in dl:
			domains.append(self.getDomain(v))

		return domains

	def getAlias(self, alias):
		pass

	def getAliasList(self, domain):
		pass

	def getAliases(self, domain):
		'''Return a list of all alias objects'''
		al = self.getAliasList(domain)
		aliases = []

		for v in al:
			aliases.append(self.getAlias(v))

		return aliases

	def deleteAlias(self, alias):
		pass
