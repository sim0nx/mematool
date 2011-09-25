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

# -*- coding: utf-8 -*-


from mematool.lib.syn2cat.singleton import Singleton
import ldap
from pylons import config, session
from mematool.lib.syn2cat.crypto import encodeAES, decodeAES


class LdapConnector(object):
	__metaclass__ = Singleton

	def __init__(self, con=None):
		if con is not None:
			self.con = con
		else:
			""" Bind to server """
			self.con = ldap.initialize(config.get('ldap.server'))
			try:
				self.con.start_tls_s()
				try:
					if 'identity' in session:
						uid = session['identity']
						binddn = 'uid=' + uid + ',' + config.get('ldap.basedn_users')
						password = decodeAES(session['secret'])

						self.con.simple_bind_s(binddn, password)
				except ldap.INVALID_CREDENTIALS:
					print "Your username or password is incorrect."
			except ldap.LDAPError, e:
				''' @TODO better handle errors and don't use "sys.exit" ;-) '''
				print e.message['info']
				if type(e.message) == dict and e.message.has_key('desc'):
					print e.message['desc']
				else:   
					print e

				# @TODO no sysexit
				sys.exit

	def getLdapConnection(self):
		return self.con

	def setLdapConnection(self, con):
		self.con = con

	def getGroup(self, cn):
		''' Get a specific group'''
		filter = '(cn=' + cn + ')'
		attrs = ['*']

		result = self.con.search_s( config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )

		if not result:
			raise LookupError('No such group !')

		group = {}
		for dn, attr in result:
			for k, v in attr.iteritems():
				group[k] = v[0]

		return group

	def getGroupList(self):
		'''Get a list of all groups'''
		filter = '(cn=*)'
		attrs = ['cn', 'gidNumber']
		
		result = self.con.search_s( config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )
		groups = {}
		
		for dn, attr in result:
			groups.append( attr['cn'][0] )

		return groups

	def getGroupMembers(self, group):
		'''Get all members of a specific group'''
		filter = '(cn=' + group + ')'
		attrs = ['memberUid']

		result = self.con.search_s(config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs)

		if not result:
			raise LookupError('No such group !')

		members = []

		for dn, attr in result:
			for key, value in attr.iteritems():
				if len(value) == 1:
					items.append(value[0])
				else:
					for i in value:
						members.append(i)

		return members

	def getMember(self, uid):
		'''Get a specific Member'''
		filter = '(uid=' + uid + ')'
		attrs = ['*']
		basedn = 'uid=' + str(uid) + ',' + str(config.get('ldap.basedn_users'))

		result = self.con.search_s( basedn, ldap.SCOPE_SUBTREE, filter, attrs )

		if not result:
			raise LookupError('No such user !')

		member = {}

		for dn, attr in result:
			for key, value in attr.iteritems():
				member[key] = value[0]

		return member

	def getUidNumberFromUid(self, uid):
		'''Get a UID-number based on its UID'''
		filter = '(uid=' + uid + ')'
		attrs = ['uidNumber']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )
		
		if not result:
			raise LookupError('No such user !')

		for dn, attr in result:
			uidNumber = attr['uidNumber'][0]

		return uidNumber

	def getMemberList(self):
		'''Get a list of all users belonging to the group "users" (gid-number = 100)
		and having a uid-number >= 1000 and < 65000'''
		filter = '(&(uid=*)(gidNumber=100))'
		attrs = ['uid', 'uidNumber']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

		members = []

		for dn, attr in result:
			if int(attr['uidNumber'][0]) >= 1000 and int(attr['uidNumber'][0]) < 65000:
				members.append( attr['uid'][0] )

		members.sort()

		return members

	# see openldap slapo-memberof
	def getActiveMemberList(self):
		'''Get a list of all users belonging to the group "users" (gid-number = 100)
		and having a uid-number >= 1000 and < 65000 and not being a member of the locked group
		i.e. active members'''
		filter = '(&(uid=*)(gidNumber=100))'
		attrs = ['uid', 'uidNumber']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

		members = []

		for dn, attr in result:
			if int(attr['uidNumber'][0]) >= 1000 and int(attr['uidNumber'][0]) < 65000:
				if not 'syn2cat_locked_member' in self.getMemberGroups( attr['uid'][0] ):
					members.append( attr['uid'][0] )

		members.sort()

		return members

	def getMemberGroups(self, uid):
		'''Get a list of groups a user is a member of'''
		filter = '(memberUid=' + uid + ')'
		attrs = ['cn']
		groups = []

		result = self.con.search_s( config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )

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
		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, config.get('ldap.uid_filter'), [config.get('ldap.uid_filter_attrs')] )

		uidNumber = -1

		for dn, attr in result:
			for key, value in attr.iteritems():
				if int(value[0]) > uidNumber and int(value[0]) < 65000:
					uidNumber = int(value[0])

		return str(uidNumber)

	def getHighestGidNumber(self):
		'''Get the highest used gid-number
		this is used when adding a new group'''
		result = self.con.search_s( config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, config.get('ldap.gid_filter'), [config.get('ldap.gid_filter_attrs')] )

		gidNumber = -1

		for dn, attr in result:
			for key, value in attr.iteritems():
				if int(value[0]) > uidNumber and int(value[0]) < 65000:
					uidNumber = int(value[0])

		return str(uidNumber)

	def prepareVolatileAttribute(self, member, attribute, encoding='utf-8'):
		'''Checks if an attribute is present in the member object and
		whether it should be updated or else deleted.
		While doing that it converts the attribute value to the specified
		encoding, which by default is UTF-8
		Returns None if the attribute it not present or nothing should be
		changed'''
		retVal = None

		if hasattr(member, attribute):
			a = getattr(member, attribute)

			if a:
				if a == 'removed':
					retVal = (ldap.MOD_DELETE, attribute, None)
				else:
					a = str(a.encode(encoding, ignore))
					retVal = (ldap.MOD_REPLACE, attribute, a)

		return retVal

	def saveMember(self, member):
		'''Save a user'''
		mod_attrs = []

		if member.cn != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'cn', str(member.cn.encode( "utf-8" ))))

		if member.sn != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'sn', str(member.sn.encode( "utf-8" ))))

		if member.gn != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'givenName', str(member.gn.encode( "utf-8" ))))

		if member.homePostalAddress != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'homePostalAddress', str(member.homePostalAddress.encode( "utf-8" ))))

		if member.homePhone != '':
			if member.homePhone == '>>REMOVE<<':
				mod_attrs.append((ldap.MOD_DELETE, 'homePhone', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'homePhone', str(member.phone)))
		# @TODO wildcard delete does not work ... fix
		#else:
		#	mod_attrs.append((ldap.MOD_DELETE, 'homePhone', None))

		if member.mobile != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'mobile', str(member.mobile)))

		if member.mail != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'mail', str(member.mail)))

		#if member.userCertificate != '':
		#	mod_attrs.append((ldap.MOD_REPLACE, 'userCertificate', str(member.userCertificate)))
		#else:
		#	mod_attrs.append((ldap.MOD_DELETE, 'userCertificate', None))

		if member.gidNumber != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'gidNumber', str(member.gidNumber)))

		if member.loginShell != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'loginShell', str(member.loginShell)))

		if member.homeDirectory != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'homeDirectory', str(member.homeDirectory)))

		if member.birthDate != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'birthDate', str(member.birthDate)))

		if member.arrivalDate != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'arrivalDate', str(member.arrivalDate)))

		if member.leavingDate != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'leavingDate', str(member.leavingDate)))
		# @TODO wildcard delete does not work ... fix
		#else:
		#	mod_attrs.append((ldap.MOD_DELETE, 'leavingDate', None))


		if member.userPassword and member.userPassword != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'userPassword', str(member.userPassword)))
			if member.sambaNTPassword and member.sambaNTPassword != '':
				mod_attrs.append((ldap.MOD_REPLACE, 'sambaNTPassword', str(member.sambaNTPassword)))

		if member.sshPublicKey:
			if member.sshPublicKey == 'removed':
				mod_attrs.append((ldap.MOD_DELETE, 'sshPublicKey', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'sshPublicKey', str(member.sshPublicKey)))

		if member.pgpKey:
			if member.pgpKey == 'removed':
				mod_attrs.append((ldap.MOD_DELETE, 'pgpKey', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'pgpKey', str(member.pgpKey)))

		if member.iButtonUID:
			if member.iButtonUID == 'removed':
				mod_attrs.append((ldap.MOD_DELETE, 'iButtonUID', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'iButtonUID', str(member.iButtonUID)))

		if member.conventionSigner:
			if member.conventionSigner == 'removed':
				mod_attrs.append((ldap.MOD_DELETE, 'conventionSigner', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'conventionSigner', str(member.conventionSigner)))

		if member.xmppID:
			if member.xmppID == 'removed':
				mod_attrs.append((ldap.MOD_DELETE, 'xmppID', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'xmppID', str(member.xmppID)))

		result = self.con.modify_s('uid=' + member.uid + ',' + config.get('ldap.basedn_users'), mod_attrs)

		self.changeUserGroup(member.uid, 'syn2cat_full_member', member.fullMember)
		self.changeUserGroup(member.uid, 'syn2cat_locked_member', member.lockedMember)


		return result

	def addMember(self, member):
		'''Add a new user'''
		# @TODO we don't set all possible attributes !!! fix
		add_record = [
				('objectclass', ['posixAccount', 'organizationalPerson', 'inetOrgPerson', 'shadowAccount', 'top', 'samsePerson', 'sambaSamAccount', 'ldapPublicKey', 'syn2catPerson']),
				('uid', [member.uid.encode('ascii','ignore')]),
				('cn', [member.cn.encode('ascii','ignore')] ),
				('sn', [member.sn.encode('ascii','ignore')] ),
				('userPassword', [member.userPassword.encode('ascii','ignore')]),
				('gidNumber', [member.gidNumber.encode('ascii','ignore')]),
				('homeDirectory', [member.homeDirectory.encode('ascii','ignore')]),
				('uidNumber', [member.uidNumber.encode('ascii','ignore')]),
				('loginShell', [member.loginShell.encode('ascii','ignore')]),
				('mobile', [member.mobile.encode('ascii','ignore')]),
				('mail', [member.mail.encode('ascii','ignore')]),
				('ou', ['People']),
				('sambaSID', [member.sambaSID.encode('ascii','ignore')]),
				('sambaNTPassword', [member.sambaNTPassword.encode('ascii','ignore')]),
				('birthDate', [member.birthDate.encode('ascii','ignore')]),
				('givenName', [member.gn.encode('ascii','ignore')]),
				('homePostalAddress', [member.homePostalAddress.encode('ascii','ignore')])
			]

		dn = 'uid=' + member.uid + ',' + config.get('ldap.basedn_users')
		dn = dn.encode('ascii','ignore')
		result = self.con.add_s( dn, add_record)

		self.changeUserGroup(member.uid, 'syn2cat_full_member', member.fullMember)
		self.changeUserGroup(member.uid, 'syn2cat_locked_member', member.lockedMember)

		return result

	def addGroup(self, gid):
		'''Add a new group'''
		new_gidnumber = self.getHighestGidNumber()
		add_record = [
				('objectclass', ['posixGroup', 'top']),
				('cn', [gid.encode('ascii','ignore')]),
				('gidNumber', [str(new_gidnumber).encode('ascii','ignore')])
			]

		dn = 'cn=' + gid + ',' + config.get('ldap.basedn_groups')
		dn = dn.encode('ascii','ignore')
		result = self.con.add_s( dn, add_record)

		return result

	def changeUserGroup(self, uid, group, status):
		'''Change user/group membership'''
		mod_attrs = []
		result = ''
		import sys

		if status:
			mod_attrs = [ (ldap.MOD_ADD, 'memberUid', uid.encode('ascii','ignore')) ]
		else:
			mod_attrs = [ (ldap.MOD_DELETE, 'memberUid', uid.encode('ascii','ignore')) ]

		try:
			result = self.con.modify_s('cn=' + group.encode('ascii','ignore') + ',' + config.get('ldap.basedn_groups'), mod_attrs)
		except (ldap.TYPE_OR_VALUE_EXISTS, ldap.NO_SUCH_ATTRIBUTE):
			pass
		except:
			print sys.exc_info()[0]
			pass

		return result
