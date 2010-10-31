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


from sqlalchemy import schema, types, orm, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Boolean, Date, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation, backref

from mematool.model.meta import Base
from mematool.lib.base import Session

from mematool.lib.syn2cat.ldapConnector import LdapConnector


# This is the association table for the many-to-many relationship between
# groups and permissions.
#group_permission_table = Table('group_permission', metadata,
#    Column('group_id', Integer, ForeignKey('group.group_id',
#        onupdate="CASCADE", ondelete="CASCADE")),
#    Column('permission_id', Integer, ForeignKey('permission.permission_id',
#        onupdate="CASCADE", ondelete="CASCADE"))
#)
#
#user_group_table = Table('user_group', metadata,
#    Column('user_id', Integer, ForeignKey('user.user_id',
#        onupdate="CASCADE", ondelete="CASCADE")),
#    Column('group_id', Integer, ForeignKey('group.group_id',
#        onupdate="CASCADE", ondelete="CASCADE"))
#)

class Group(Base):
	
	gid = ''
	groupName = ''

	#members = relation('Member', secondary=user_group_table, backref='groups')
	
	def __repr__(self):
		return "<Group('gid=%d, groupName=%s')>" % (self.gid, self.groupName)

	def loadFromLdap(self):
                self.ldapcon = LdapConnector()
		group = self.ldapcon.getGroup(self.gid)
		if 'groupName' in group:
			group.groupName = group['groupName']


class Permission(Base):
	__tablename__ = 'permission'
	__table_args__ = (
		{'mysql_engine':'InnoDB'}
		)

	idpermission = Column(Integer, autoincrement=True, primary_key=True)
	dtname = Column(String(40))
	dtldapgid = Column(Integer)
	## of course, if you have a secondary table, you don't need the ldapgid column
	## also, secondary tables seem necessary for many to many relations, as in this case.
	#groups = relation(Group, secondary=group_permission_table,backref='permissions')

	def __init__(self):
		pass	

	def __repr__(self):
		return "<Permission('idpermission=%d, dtldapgroup=%s')>" % (self.idpermission, self.dtldapgroup)


	def save(self):
		Session.commit()

