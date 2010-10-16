from sqlalchemy import schema, types, orm, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation
from mematool.model.meta import Base

from mematool.lib.base import Session

from mematool.lib.syn2cat.ldapConnector import LdapConnector
import hashlib
from base64 import encodestring as encode
from base64 import decodestring as decode
import os




class Member(Base):
	__tablename__ = 'member'
	__table_args__ = (
		{'mysql_engine':'InnoDB'}
		)

	idmember = Column(Integer, primary_key=True)
	dtusername = Column(String(255))
	# ldap
	cn = ''    # fullname
	sn = ''    # family name
	gn = ''    # given name
	address = '' # complete address (homePostalAddress)
	phone = '' # phone (homePhone)
	mobile = '' # mobile
	mail = '' # mail
	userPassword = '' # SSHA password
	sambaNTPassword = '' # NT Password
	userCertificate = '' # x509 certificate
	uidNumber = '' # user id (uidNumber)
	gidNumber = '' # group id (gidNumber)
	loginShell = '' # login shell
	homeDirectory = '' # homeDirectory
	birthDate = '' # birthDate
	arrivalDate = '' # member since
	leavingDate = '' # membership canceled
	


	def __init__(self):
		pass

	def __repr__(self):
		return "<Member('idmember=%s, dtusername=%s')>" % (self.idmember, self.dtusername)


	def loadFromLdap(self):
		self.ldapcon = LdapConnector()
		member = self.ldapcon.getMember(self.dtusername)

		if 'cn' in member:
			self.cn = member['cn']
		if 'sn' in member:
			self.sn = member['sn']
		if 'givenName' in member:
			self.gn = member['givenName']
		if 'homePostalAddress' in member:
			self.address = member['homePostalAddress']
		if 'homePhone'  in member:
			self.phone = member['homePhone']
		if 'mobile'  in member:
			self.mobile = member['mobile']
		if 'mail'  in member:
			self.mail = member['mail']
		if 'certificate'  in member:
			self.userCertificate = member['certificate']
		if 'gidNumber'  in member:
			self.gidNumber = member['gidNumber']
		if 'uidNumber'  in member:
                        self.uidNumber = member['uidNumber']
                if 'loginShell'  in member:
                        self.loginShell = member['loginShell']
		if 'homeDirectory'  in member:
			self.homeDirectory = member['homeDirectory']
		if 'birthDate'  in member:
			self.birthDate = member['birthDate']
		if 'arrivalDate'  in member:
			self.arrivalDate = member['arrivalDate']
		if 'leavingDate'  in member:
			self.leavingDate = member['leavingDate']


	def save(self):
		self.ldapcon = LdapConnector()

		if self.gn == '':
			self.gn = '_'

		if self.mobile == '':
			self.mobile = '0'

		self.ldapcon.saveMember(self)

		m = Session.query(Member).filter(Member.idmember == self.idmember).one()
		m.dtusername = self.dtusername
		Session.commit()


	def setPassword(self, password):
		salt = os.urandom(4)
		h = hashlib.sha1(password)
		h.update(salt)
		self.userPassword = "{SSHA}" + encode(h.digest() + salt)
		self.sambaNTPassword = hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()
