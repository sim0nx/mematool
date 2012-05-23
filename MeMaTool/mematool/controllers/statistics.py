#
# MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
# This file is part of MeMaTool.
#
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.


import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect
from pylons import config
from pylons.i18n.translation import _

from mematool.lib.base import BaseController, render, Session
from mematool.model import Member, TmpMember, Payment

log = logging.getLogger(__name__)

from mematool.model.ldapModelFactory import LdapModelFactory
import re
from mematool.lib.syn2cat import regex
from mematool.lib.syn2cat.crypto import encodeAES

from sqlalchemy import and_
from datetime import date, datetime

from webob.exc import HTTPUnauthorized


class StatisticsController(BaseController):

  def __init__(self):
    super(StatisticsController, self).__init__()
    self.lmf = LdapModelFactory()

  def __before__(self):
    super(StatisticsController, self).__before__()

    if not self.identity:
      redirect(url(controller='error', action='forbidden'))

  def _require_auth(self):
    return True

  @BaseController.needAdmin
  def index(self):
    c.heading = _('Statistics')

    c.members = len(self.lmf.getUserList())
    activeMembers = self.lmf.getActiveMemberList()
    c.activeMembers = len(activeMembers)
    c.formerMembers = c.members - c.activeMembers

    c.paymentsOk = 0

    for uid in activeMembers:
      last_payment = None

      try:
        last_payment = Session.query(Payment).filter(and_(Payment.uid == uid, Payment.verified == 1)).order_by(Payment.date.desc()).limit(1)[0]
      except Exception as e:
        ''' Don't care if there is no payment '''
        print e
        print uid
        pass

      if last_payment:
        d = last_payment.date
        today = datetime.now().date()

        if d.year > today.year or (d.year == today.year and d.month >= today.month):
          c.paymentsOk += 1

    c.paymentsNotOk = c.activeMembers - c.paymentsOk

    return render('/statistics/index.mako')
