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


		result = self.con.modify_s('uid=' + member.dtusername + ',' + config.get('ldap.basedn_users'), mod_attrs)

		return result
