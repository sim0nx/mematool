from paste.httpexceptions import HTTPFound
from mematool.model.member import Member

class MemberModelPlugin(object):

	def authenticate(self, environ, identity):
		try:
			pass
			# do ldap auth here
		except LdapError:
			return None

		return success

	def add_metadata(self, environ, identity):
		""" retrieve metadata from the Member model """
		userid = identity.get('repoze.who.userid')
		user = Member.get(userid)	# idmember is primary key for member

		if user is not None:
			identity['user'] = user
