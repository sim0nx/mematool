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

import cherrypy
import logging
from sqlalchemy import and_
import datetime
from mematool.controllers import BaseController, TemplateContext
from mematool.helpers.i18ntool import ugettext as _
from mematool.model.dbmodel import Payment

log = logging.getLogger(__name__)


class StatisticsController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(StatisticsController, self).__init__()

  @cherrypy.expose()
  @BaseController.needAdmin
  def index(self):
    c = TemplateContext()
    c.heading = _('Statistics')

    c.members = len(self.mf.getUserList())
    activeMembers = self.mf.getActiveMemberList()
    c.activeMembers = len(activeMembers)
    c.formerMembers = c.members - c.activeMembers

    c.paymentsOk = 0

    for uid in activeMembers:
      last_payment = None

      try:
        last_payment = self.db.query(Payment).filter(and_(Payment.uid == uid, Payment.verified == 1)).order_by(Payment.date.desc()).limit(1)[0]
      except Exception as e:
        ''' Don't care if there is no payment '''
        pass

      if last_payment:
        d = last_payment.date
        today = datetime.datetime.now().date()

        if d.year > today.year or (d.year == today.year and d.month >= today.month):
          c.paymentsOk += 1

    c.paymentsNotOk = c.activeMembers - c.paymentsOk

    return self.render('/statistics/index.mako', template_context=c)
