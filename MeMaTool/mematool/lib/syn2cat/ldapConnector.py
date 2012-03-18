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


import ldap
from pylons import config, session
from mematool.lib.syn2cat.crypto import encodeAES, decodeAES

class InvalidCredentials(Exception):
	pass

class ServerError(Exception):
	pass

class LdapConnector(object):
	def __init__(self, con=None, uid=None, password=None, cnf=None):
		self.con = None

		if cnf is not None:
			self.cnf = cnf
		else:
			self.cnf = config

		if con is not None:
			self.con = con
		else:
			""" Bind to server """
			self.con = ldap.initialize(self.cnf.get('ldap.server'))
			try:
				self.con.start_tls_s()
				try:
					try:
						if session and 'identity' in session:
							uid = session['identity']
							password = decodeAES(session['secret'])
					except:
						pass

					if not (uid is None or password is None):
						binddn = 'uid=' + uid + ',' + self.cnf.get('ldap.basedn_users')
						self.con.simple_bind_s(binddn, password)
				except ldap.INVALID_CREDENTIALS:
					print "Your username or password is incorrect."
					raise InvalidCredentials()
			except ldap.LDAPError, e:
				''' @TODO better handle errors and don't use "sys.exit" ;-) '''
				print e.message['info']
				if type(e.message) == dict and e.message.has_key('desc'):
					print e.message['desc']
				else:   
					print e

				raise ServerError()

	def getLdapConnection(self):
		return self.con

	def setLdapConnection(self, con):
		self.con = con
