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

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from mematool.lib.base import BaseController, render, Session
from mematool.model.payment import Payment

from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

class PaymentsController(BaseController):

	def __init__(self):
		pass

	def index(self):
		return self.showOutstanding()
        
	def showOutstanding(self):
		""" Show which users still need to pay their membership fees and if a reminder has already been sent """
		return render('/payments/showOutstanding.mako')
    	
	def showPayments(self):
		""" Show a specific user's payments """
		if (not 'member_id' in request.params):
			redirect(url(controller='payments', action='showOutstanding'))

		c.heading = 'Payments'

		payment_q = Session.query(Payment).filter(Payment.limember == request.params['member_id'])

                try:
                        payment = payment_q.one()
			for i in payment:
				print "%s" % payment[i]
		except NoResultFound:
			print "oops"
		    
		return render('/payments/showPayments.mako')

	def addPayment(self):
		""" Add a payment to a specific user """
		if (not 'member_id' in request.params):
			#display dropdown on null value
			print "no member id supplied"
		else:
			#select name from dropdown
			print "You selected member id %s" % request.params['member_id']

		return render('/payments/addPayment.mako')
