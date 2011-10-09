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


from sqlalchemy import schema, types, orm, create_engine, Table, Column, Integer, Float, String, MetaData, ForeignKey, Boolean, Date, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation

from mematool.model.meta import Base
from mematool.model.paymentmethod import Paymentmethod
from mematool.lib.base import Session

class Payment(Base):
	__tablename__ = 'payment'
	__table_args__ = (
		{'mysql_engine':'InnoDB'}
		)

	idpayment = Column(Integer, primary_key=True)
	member_id = Column(String(255))
	dtreason = Column(String(255))
	dtdate = Column(Date, nullable=False)
	dtamount = Column(Float, nullable=False)
	dtverified = Column(Boolean)
	lipaymentmethod = Column(Integer, ForeignKey('paymentmethod.idpaymentmethod'))
	paymentperiod = Column(Integer, ForeignKey('paymentperiod.id_'))

	# Members can have many payments, thus the foreign key belongs here
	#limember = Column(Integer, ForeignKey('member.idmember'))
	dtpaymentmethod = relation(Paymentmethod, primaryjoin=lipaymentmethod == Paymentmethod.idpaymentmethod)
	
	# trying to set up the relation in the Member class
	#limember = relation(Member, backref=backref('payments', order_by=idpayment))

	#def __init__(self,reason,date,amount,limethod,limember):
	def __init__(self):
		pass	

	def __repr__(self):
		return "<Payment('idpayment=%d, member=%s', dtdate=%s, dtverified=%d)>" % (self.idpayment, self.member_id, self.dtdate, self.dtverified)


	def save(self):
		Session.commit()


class PaymentPeriod(Base):
	__tablename__ = 'paymentperiod'
	__table_args__ = (
		{'mysql_engine':'InnoDB'}
		)

	id = Column(Integer, primary_key=True)
	member_id = Column(String(255))
	start = Column(Date, nullable=False)
	end = Column(Date, nullable=False)


	def __init__(self):
		pass	

	def __repr__(self):
		return "<PaymentPeriod('id=%d, member=%s', start=%s, end=%s)>" % (self.id, self.member_id, self.start, self.end)
