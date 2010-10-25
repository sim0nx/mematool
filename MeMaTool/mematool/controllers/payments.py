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

from formencode import htmlfill
from mematool.model.schema.payments import PaymentForm

from pylons.decorators import validate
from pylons.decorators.rest import restrict

from mematool.lib.base import BaseController, render, Session
from mematool.model import Payment, Member, Paymentmethod

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

		## ideally, fetch monthly from member and the rest from payment (one to many relation)
		## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html
		payment_q = Session.query(Payment).filter(Payment.limember == request.params['member_id'])

		## having problems establishing relations
		member_q = Session.query(Member).filter(Member.idmember == request.params['member_id'])
		
		## using a join while trying to figure out how to make relations work (can't get this to work either)
		#query = Session.query(Member,Payment).filter(Payment.limember == Member.idmember).filter(Member.idmember == request.params['member_id'])

                try:
			#member,payments = query.all()
			c.member = member_q.one()
			c.until = '06.2011'
			c.payments = payment_q.all()
			c.member_id = request.params['member_id']

		except NoResultFound:
			print "oops"
		    
		return render('/payments/listPayments.mako')

	def editPayment(self):
		""" Add or edit a payment to/of a specific user """

		if (not 'idpayment' in request.params):
			c.payment = Payment()
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

		c.methods = Session.query(Paymentmethod).all()
		c.heading = 'Adding payment for user %s' % member_id

		return render('/payments/editPayment.mako')


	# I suspect keyError catching only works with forms in editPayment created by the FormBuild module
	@restrict('POST')
	@validate(schema=PaymentForm(), form='editPayment')
	def savePayment(self):
		""" Save a new or edited payment """

		if (self.form_result['idpayment'] != 0):
			np = Session.query(Payment).filter(Payment.idpayment == request.params['idpayment']).one()
		else:
			np = Payment()

		for key, value in self.form_result.items():
			setattr(np, key, value)

		Session.add(np)
		np.save() # defined in Payment model
		## how to test for success? --> if np.idpayment set
		#print(repr(np.idpayment))

		session['flash'] = 'Payment saved successfully.'
		session.save()

		redirect(url(controller='payments', action='listPayments', member_id=self.form_result['limember']))
