# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Georges Toth <georges _at_ trypill _dot_ org>
#
# This file is part of MeMaTool.
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MeMaTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Unicode
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Payment(Base):
  __tablename__ = 'payment'

  id = Column(Integer, primary_key=True)
  uid = Column(String(255))
  date = Column(Date, nullable=False)
  verified = Column(Boolean)
  status = Column(Integer(1))

  def __repr__(self):
    return "<Payment('id=%d, uid=%s', date=%s, verified=%d, status%s)>" % (self.id, self.uid, self.date, self.verified, self.status)


class Group(Base):
  '''Table containing managed groups'''
  __tablename__ = 'group'

  id = Column(Integer, primary_key=True)
  gid = Column(String(255))

  def __repr__(self):
    return "<Group('id=%d, gid=%s')>" % (self.id, self.gid)

  @property
  def cn(self):
    return self.gid


class Paymentmethod(Base):
  __tablename__ = 'paymentmethod'

  idpaymentmethod = Column(Integer, primary_key=True)
  dtname = Column(String(255))

  def __repr__(self):
    return "<Paymentmethod('idpaymentmethod=%d, dtname=%s')>" % (self.idpaymentmethod, self.dtname)


class Preferences(Base):
  __tablename__ = 'preferences'

  id = Column(Integer, primary_key=True)
  uidNumber = Column(Integer, index=True)
  last_change = Column(DateTime, nullable=False)
  key = Column(String(255))
  value = Column(String(255))

  def __repr__(self):
    return "<Preferences('uidNumber=%d, last_change=%s, key=%s, value=%s)>" % (self.uidNumber, self.last_change, self.key, self.value)


class TmpMember(Base):
  __tablename__ = 'tmpMember'

  id = Column(Integer, primary_key=True)
  gn = Column(Unicode(60))
  sn = Column(Unicode(60))
  homePostalAddress = Column(Unicode(255))
  phone = Column(Unicode(30))
  mobile = Column(Unicode(30))
  mail = Column(Unicode(255))
  xmppID = Column(Unicode(255))

  def __init__(self, uidNumber):
    self.id = uidNumber

  def __str__(self):
    return "<TmpMember('id=%d, gn=%s', sn=%s, homePostalAddress=%s, phone=%s, mobile=%s, mail=%s, xmppID=%s)>" % (self.id, self.gn, self.sn, self.homePostalAddress, self.phone, self.mobile, self.mail, self.xmppID)
