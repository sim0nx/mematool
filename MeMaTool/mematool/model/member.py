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

import hashlib
from binascii import b2a_base64, a2b_base64
import os


class Member():
	# ldap
	str_vars = ['uid',\
		'cn',\
		'sn',\
		'givenName',\
		'homePhone',\
		'mobile',\
		'mail',\
		'xmppID',\
		'userPassword',\
		'sambaNTPassword',\
		'sambaSID',\
		'sshPublicKey',\
		'pgpKey',\
		'iButtonUID',\
		'conventionSigner',\
		'uidNumber',\
		'gidNumber',\
		'loginShell',\
		'hDirectory',\
		'birthDate',\
		'hPostalAddress',\
		'arrivalDate',\
		'leavingDate']
	list_vars = ['groups']
	bool_vars = ['fullMember',\
		'lockedMember']

	'''
	uid = ''   # uid
	cn = ''	# fullname
	sn = ''	# family name
	givenName = ''	# given name
	homePhone = '' # phone (homePhone)
	mobile = '' # mobile
	mail = '' # mail
	xmppID = '' # xmppID
	userPassword = '' # SSHA password
	sambaNTPassword = '' # NT Password
	sambaSID = ''
	sshPublicKey = '' # SSH public key
	pgpKey = '' # PGP key
	iButtonUID = '' # iButton UID
	conventionSigner = '' # Member convention signer
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
	'''
	

	def __init__(self):
		for v in self.str_vars:
			setattr(self, v, '')
		for v in self.list_vars:
			setattr(self, v, [])
		for v in self.bool_vars:
			setattr(self, v, False)

		self.all_vars = []
		self.all_vars.extend(self.str_vars)
		self.all_vars.extend(self.list_vars)
		self.all_vars.extend(self.bool_vars)

		self.validate = False        # validation needed ?

	def __str__(self):
		return "<Member('uidNumber=%s, uid=%s')>" % (self.uidNumber, self.uid)

	def __eq__(self, om):
		equal = True

		for v in self.all_vars:
			if not getattr(self, v) == getattr(om, v):
				equal = False
				break

		return equal

	def __ne__(self, om):
		return not self == om

	@property
	def validate(self):
		if self.uidNumber:
			if (Session.query(TmpMember).filter(TmpMember.id == self.uidNumber).count() > 0):
				return True

		return False

	@property
	def gn(self):
		return self.givenName

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
