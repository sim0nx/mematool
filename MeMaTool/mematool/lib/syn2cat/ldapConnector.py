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


from mematool.lib.syn2cat.singleton import Singleton
import ldap
from pylons import config


class LdapConnector(object):
	__metaclass__ = Singleton


	def __init__(self):
		""" Bind to server """
		self.con = ldap.initialize(config.get('ldap.server'))
		try:
			self.con.start_tls_s()
			try:
				self.con.simple_bind_s(config.get('ldap.bind'), config.get('ldap.password'))
			except ldap.INVALID_CREDENTIALS:
				print "Your username or password is incorrect."
		except ldap.LDAPError, e:
			''' @TODO better handle errors and don't use "sys.exit" ;-) '''
			print e.message['info']
			if type(e.message) == dict and e.message.has_key('desc'):
				print e.message['desc']
			else:   
				print e

			sys.exit


	def getLdapConnection(self):
		return self.con


	def getGroup(self, cn):
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
		filter = '(cn=*)'
		attrs = ['cn', 'gidNumber']
		
		result = self.con.search_s( config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )
		groups = {}
		
		for dn, attr in result:
			groups.append( attr['cn'][0] )

		return groups


	def getGroupMembers(self, group):
		filter = '(cn=' + group + ')'
		attrs = ['memberUid']

		result = self.con.search_s( config.get('ldap.basedn_groups'), ldap.SCOPE_SUBTREE, filter, attrs )
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
		filter = '(uid=' + uid + ')'
		attrs = ['*']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

		if not result:
			raise LookupError('No such user !')

		member = {}

		for dn, attr in result:
			for key, value in attr.iteritems():
				member[key] = value[0]

		return member


	def getUidNumberFromUid(self, uid):
		filter = '(uid=' + uid + ')'
		attrs = ['uidNumber']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )
		
		if not result:
			raise LookupError('No such user !')

		for dn, attr in result:
			uidNumber = attr['uidNumber'][0]

		return uidNumber


	def getMemberList(self):
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
		filter = '(&(uid=*)(gidNumber=100))'
		attrs = ['uid', 'uidNumber']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

		members = []

		for dn, attr in result:
			if int(attr['uidNumber'][0]) >= 1000 and int(attr['uidNumber'][0]) < 65000:
				if not 'syn2cat_locked_member' in self.getMemberGroups( attr['uid'][0] ):
					members.append( [attr['uid'][0], attr['uidNumber'][0]] )

		members.sort()

		return members


	def getMemberGroups(self, member):
		filter = '(memberUid=' + member + ')'
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


	def saveMember(self, member):
		mod_attrs = []

		if member.cn != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'cn', str(member.cn)))

		if member.sn != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'sn', str(member.sn)))

		if member.gn != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'givenName', str(member.gn)))

		if member.homePostalAddress != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'homePostalAddress', str(member.homePostalAddress)))

		if member.phone != '':
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


		result = self.con.modify_s('uid=' + member.uid + ',' + config.get('ldap.basedn_users'), mod_attrs)

		return result
