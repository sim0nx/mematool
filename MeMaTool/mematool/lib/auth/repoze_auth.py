from paste.httpexceptions import HTTPFound
from mematool.model.member import Member

class LdapAuthPlugin(object):

	def __init__(self):
		pass

	def authenticate(self, environ, identity):
		try:
			login = identity['login']
			password = identity['password']
		except KeyError:
			return None

		try:
			# do ldap auth here
		except LdapError:
			return None

		return success

	def _checkLdapCredentisals(self, environ, identity):
		return 

	def add_metadata(self, environ, identity):
		""" retrieve metadata from the Member model """
		userid = identity.get('repoze.who.userid')
		user = Member.get(userid)	# idmember is primary key for member

		if user is not None:
			identity['user'] = user
