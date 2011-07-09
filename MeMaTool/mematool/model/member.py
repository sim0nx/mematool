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


from mematool.model.meta import Base

from datetime import date
from mematool.lib.base import Session
from mematool.model import TmpMember

from mematool.lib.syn2cat.ldapConnector import LdapConnector
import hashlib
from binascii import b2a_base64, a2b_base64
import os


class Member():
	# ldap
	uid = ''   # uid
	cn = ''	# fullname
	sn = ''	# family name
	gn = ''	# given name
	homePhone = '' # phone (homePhone)
	mobile = '' # mobile
	mail = '' # mail
	userPassword = '' # SSHA password
	sambaNTPassword = '' # NT Password
	sambaSID = ''
	#userCertificate = '' # x509 certificate
	sshPublicKey = '' # SSH public key
	uidNumber = '' # user id (uidNumber)
	gidNumber = '' # group id (gidNumber)
	loginShell = '' # login shell
	homeDirectory = '' # homeDirectory
	birthDate = '' # birthDate
	homePostalAddress = '' # homePostalAddress
	arrivalDate = '' # member since
	leavingDate = '' # membership canceled
	groups = [] # additional user groups
	fullMember = False
	lockedMember = False
	validate = False	# validation needed ?

	

	def __init__(self, uid=None):
		if uid is not None:
			self.uid = uid
			self.loadFromLdap()

			if (Session.query(TmpMember).filter(TmpMember.id == self.uidNumber).count() > 0):
				self.validate = True


	def __str__(self):
		return "<Member('uidNumber=%s, uid=%s')>" % (self.uidNumber, self.uid)


	def loadFromLdap(self):
		self.ldapcon = LdapConnector()
		member = self.ldapcon.getMember(self.uid)

		if 'cn' in member:
			self.cn = member['cn']
		if 'sn' in member:
			self.sn = member['sn']
		if 'givenName' in member:
			self.gn = member['givenName']
		if 'homePostalAddress' in member:
			self.homePostalAddress = member['homePostalAddress']
		if 'homePhone'  in member:
			self.phone = member['homePhone']
		if 'mobile'  in member:
			self.mobile = member['mobile']
		if 'mail'  in member:
			self.mail = member['mail']
		if 'sambaNTPassword' in member and member['sambaNTPassword'] != '':
			self.sambaNTPassword = 'yes'
		if 'sambaSID' in member and member['sambaSID'] != '':
			self.sambaSID = member['sambaSID']
		#if 'certificate'  in member:
		#	self.userCertificate = member['certificate']
		if 'sshPublicKey' in member:
			self.sshPublicKey = member['sshPublicKey']
		if 'gidNumber'  in member:
			self.gidNumber = member['gidNumber']
		if 'uidNumber' in member:
			self.uidNumber = member['uidNumber']
		if 'loginShell'  in member:
			self.loginShell = member['loginShell']
		if 'homeDirectory'  in member:
			self.homeDirectory = member['homeDirectory']
		if 'birthDate'  in member:
			self.birthDate = member['birthDate']
		if 'homePostalAddress' in member:
			self.homePostalAddress = member['homePostalAddress']
		if 'arrivalDate'  in member:
			self.arrivalDate = member['arrivalDate']
		if 'leavingDate'  in member:
			self.leavingDate = member['leavingDate']

		self.groups = self.ldapcon.getMemberGroups(self.uid)
		if 'syn2cat_full_member' in self.groups:
			self.fullMember = True
		if 'syn2cat_locked_member' in self.groups:
			self.lockedMember = True


	def save(self):
		self.ldapcon = LdapConnector()

		if self.gn == '':
			self.gn = '_'

		if self.mobile == '':
			self.mobile = '0'

		self.ldapcon.saveMember(self)


	def add(self):
		self.ldapcon = LdapConnector()

		if self.gn == '':
			self.gn = '_'

		if self.mobile == '':
			self.mobile = '0'

		self.uidNumber = self.ldapcon.getHighestUidNumber()
		self.generateUserSID()
		self.ldapcon.addMember(self)


	def setPassword(self, password):
		salt = os.urandom(4)
		h = hashlib.sha1(password)
		h.update(salt)
		self.userPassword = '{SSHA}' + b2a_base64(h.digest() + salt)[:-1]
		self.sambaNTPassword = hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()


	def generateUserSID(self):
		#@TODO put in config file
		serverSambaSID = 'S-1-1-1'
		self.sambaSID = serverSambaSID + '-' + str( (int(self.uidNumber) * 2) + 1000 )
