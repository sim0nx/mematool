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
		self.con = ldap.initialize(config.get('ldap.server'))
		try:
			self.con.start_tls_s()
			try:
				self.con.simple_bind_s(config.get('ldap.bind'), config.get('ldap.password'))
			except ldap.INVALID_CREDENTIALS:
				print "Your username or password is incorrect."
		except ldap.LDAPError, e:
			print e.message['info']
			if type(e.message) == dict and e.message.has_key('desc'):
				print e.message['desc']
			else:   
				print e

			sys.exit


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


	def getMemberList(self):
		filter = '(uid=*)'
		attrs = ['uid', 'uidNumber']

		result = self.con.search_s( config.get('ldap.basedn_users'), ldap.SCOPE_SUBTREE, filter, attrs )

		members = []

		for dn, attr in result:
			if int(attr['uidNumber'][0]) >= 1000 and int(attr['uidNumber'][0]) < 65000:
				members.append( attr['uid'][0] )

		return members


	def saveMember(self, member):
		mod_attrs = [ (ldap.MOD_REPLACE, 'cn', str(member.cn)),
				(ldap.MOD_REPLACE, 'sn', str(member.sn)),
	                        (ldap.MOD_REPLACE, 'homeDirectory', str(member.homeDirectory)),
	                        (ldap.MOD_REPLACE, 'mobile', str(member.mobile)),
	                        (ldap.MOD_REPLACE, 'givenName', str(member.gn))
			]

		

		if member.userPassword and member.userPassword != '':
			mod_attrs.append((ldap.MOD_REPLACE, 'userPassword', str(member.userPassword)))
			if member.sambaNTPassword and member.sambaNTPassword != '':
				mod_attrs.append((ldap.MOD_REPLACE, 'sambaNTPassword', str(member.sambaNTPassword)))

		if member.sshPublicKey:
			if member.sshPublicKey == 'removed':
				mod_attrs.append((ldap.MOD_DELETE, 'sshPublicKey', None))
			else:
				mod_attrs.append((ldap.MOD_REPLACE, 'sshPublicKey', str(member.sshPublicKey)))


		result = self.con.modify_s('uid=' + member.dtusername + ',' + config.get('ldap.basedn_users'), mod_attrs)

		return result
