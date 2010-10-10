from sqlalchemy import schema, types, orm, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean, DateTime, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation
from mematool.model.meta import Base


class Member(Base):
	__tablename__ = 'member'
	__table_args__ = (
		{'mysql_engine':'InnoDB'}
		)

	idmember = Column(Integer, primary_key=True)
	dtusername = Column(String(255))
    


	def __init__(self, idmember, dtusername):
		# sql
		self.idmember = idmember # uidNumber
		self.dtusername = dtusername # uid

		# ldap
		self.cn = ""	# fullname
		self.sn = ""	# family name
		self.gn = ""	# given name
		self.address = "" # complete address (homePostalAddress)
		self.phone = "" # phone (homePhone)
		self.mobile = "" # mobile
		self.mail = "" # mail
		self.userPassword = "" # SSHA password
		self.userCertificate = "" # x509 certificate
		self.gidNumber = "" # group id (gidNumber)
		self.homeDirectory = "" # homeDirectory
		self.birthDate = "" # birthDate
		self.arrivalDate = "" # member since
		self.leavingDate = "" # membership canceled
		pass

	def __repr__(self):
		return "<Member('idmember=%s, dtusername=%s')>" % (self.idmember, self.dtusername)
