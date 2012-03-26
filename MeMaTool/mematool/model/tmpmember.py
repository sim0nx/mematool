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
from sqlalchemy.types import Unicode
from mematool.model.meta import Base


class TmpMember(Base):
  __tablename__ = 'tmpMember'
  __table_args__ = (
    {'mysql_engine':'InnoDB'}
    )

  id      = Column(Integer, primary_key=True)
  gn      = Column(Unicode(60))
  sn      = Column(Unicode(60))
  birthDate   = Column(Unicode(10))
  homePostalAddress = Column(Unicode(255))
  phone     = Column(Unicode(30))
  mobile      = Column(Unicode(30))
  mail      = Column(Unicode(255))
  xmppID      = Column(Unicode(255))

  def __init__(self, uidNumber):
    self.id = uidNumber

  def __str__(self):
    return "<TmpMember('id=%d, gn=%s', sn=%s, birthDate=%s, homePostalAddress=%s, phone=%s, mobile=%s, mail=%s, xmppID=%s)>" % (self.id, self.gn, self.sn, self.birthDate, self.homePostalAddress, self.phone, self.mobile, self.mail, self.xmppID)
