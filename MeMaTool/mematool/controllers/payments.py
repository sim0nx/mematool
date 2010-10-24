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
    	
	def listPayments(self):
		""" Show a specific user's payments """
		if (not 'member_id' in request.params):
			redirect(url(controller='payments', action='showOutstanding'))

		c.heading = 'Payments for user %s' % request.params['member_id']

		payment_q = Session.query(Payment).filter(Payment.limember == request.params['member_id'])

                try:
                        payments = payment_q.all()
			c.payments = payments
			c.member_id = request.params['member_id']
		except NoResultFound:
			print "oops"
		    
		return render('/payments/listPayments.mako')

	def editPayment(self):
		""" Add or edit a payment to/of a specific user """

		if (not 'idpayment' in request.params):
			#new payment
			c.payment.limember = request.params['member_id']
			member_id = request.params['member_id']
		else:
			payment_q = Session.query(Payment).filter(Payment.idpayment == request.params['idpayment'])
			try:
				payment = payment_q.one()
				c.payment = payment
				member_id = payment.limember
			except NoResultFound:
				print "oops"

		c.heading = 'Adding payment for user %s' % member_id

		return render('/payments/editPayment.mako')

	#@checkdecorator	# check that payments are not in the future
	def savePayment(self):
		# do stuff
		session['flash'] = 'Payment successfully saved.'
		session.save()

		redirect(url(controller='payments',action='listPayments'))
