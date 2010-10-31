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
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from formencode import htmlfill

from mematool.model.schema.payments import PaymentForm
from mematool.lib.base import BaseController, render, Session
from mematool.model import Payment, Member, Paymentmethod

#from mematool.model.auth import Permission

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from webob.exc import HTTPUnauthorized
from datetime import date

# Decorators
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from repoze.what.predicates import has_permission
from repoze.what.plugins.pylonshq import ActionProtector, ControllerProtector

import dateutil.parser
import datetime


class PaymentsController(BaseController):
	## using this is the same as decorating __before__ with ActionController (workaround for python < 2.6)
	#PaymentsController = ControllerProtector(has_permission('admin')) (PaymentsController)
	## but it doesn't really work either

	def __init__(self):
		pass

	#@ActionProtector(has_permission('admin'))
	def __before__(self, action, **param):
		# called before accessing any method
		# also remember that any private methods (def _functionname) cannot be accessed as action
		if self.identity is None:
                        raise HTTPUnauthorized()

	def index(self):
		return self.showOutstanding()

	#@ActionProtector(has_permission('admin'))
	def verifyPayment(self):
		""" action triggered through ajax by checking/unchecking checkboxes"""
		pass
        
	def showOutstanding(self):
		""" Show which users still need to pay their membership fees and if a reminder has already been sent """

		try:
			nummissing = Session.query(Payment).filter("dtdate<:now AND dtverified=:verified AND dtmode=:mode").params(now=date.today(),verified=0,mode='recurring').count()
			nummissing += 0
			c.heading = "%d outstanding payments" % nummissing
		except NoResultFound:
			return 'No unpaid fees'
		
		# Prepare add payment form
		c.member_ids = []
		c.members = []
		for id, username in Session.query(Member.idmember, Member.dtusername).order_by(Member.dtusername):
			m = Member()
			m.dtusername = username
			m.loadFromLdap()
			last_payment = None

			try:
				last_payment = Session.query(Payment).filter(and_(Payment.limember == id, Payment.dtverified == 1)).order_by(Payment.dtdate.desc()).limit(1)[0]
			except:
				''' Don't care if there is no payment '''
				pass


			paymentGood = 'no'

			if last_payment:
				d1 = dateutil.parser.parse(str(last_payment.dtdate))
				today = str(datetime.date.today()) + ' 00:00:00'
				d2 = dateutil.parser.parse(today)

				if d1 >= d2:
					paymentGood = 'yes'


			c.members.append([id, username, m.sn, m.gn, paymentGood])
			c.member_ids.append([id, username])


		return render('/payments/showOutstanding.mako')


	def listPayments(self):
		""" Show a specific user's payments """
		if (not 'member_id' in request.params):
			redirect(url(controller='payments', action='showOutstanding'))

		c.heading = 'Payments for user %s' % request.params['member_id']

		## ideally, fetch monthly from member and the rest from payment (one to many relation)
		## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html
		payment_q = Session.query(Payment).filter(Payment.limember == request.params['member_id'])

		## having problems establishing relations, thus doing a second query
		member_q = Session.query(Member).filter(Member.idmember == request.params['member_id'])
		
		## using a join while trying to figure out how to make relations work (can't get this to work either)
		#query = Session.query(Member,Payment).filter(Payment.limember == Member.idmember).filter(Member.idmember == request.params['member_id'])

		## consider pagination
		# http://pylonsbook.com/en/1.1/starting-the-simplesite-tutorial.html#using-pagination
                try:
			member = member_q.one()
			member.loadFromLdap()
			c.member = member
			c.member_id = member.dtusername
			#c.member.leavingDate = date(int(member.leavingDate[:4]),int(member.leavingDate[5:6]),int(member.leavingDate[7:8]))
			c.payments = payment_q.all()
		
			c.unverifiedPledges = 0
			for payment in c.payments:
				if payment.dtverified == 0 and payment.dtmode == 'recurring':
					c.unverifiedPledges += 1

			## hmm this doesn't raie NoResultFound but has None as value of lastpayment
			lastpayment = payment_q.order_by(Payment.idpayment).first()
			c.ppm = lastpayment.dtrate

		except AttributeError, e:
			return 'This member has made no payments o.O ?!: %s' % e
		except NoResultFound:
			return "oops"	## replace by "this member has made no payments" message
		    
		session['return_to'] = ('payments','listPayments')
		session.save()
		return render('/payments/listPayments.mako')


	def editPayment(self):
		""" Add or edit a payment to/of a specific user """

		# vary form depending on mode (do that over ajax)

		if (not 'idpayment' in request.params):
			c.payment = Payment()
			c.payment.limember = request.params['member_id']
			action = 'Adding'
		else:
			action = 'Editing'
			payment_q = Session.query(Payment).filter(Payment.idpayment == request.params['idpayment'])
			try:
				payment = payment_q.one()
				c.payment = payment
			except NoResultFound:
				print "oops"

		methods = Session.query(Paymentmethod).all()
		## how to easily turn a result object into a list? (more efficiently than this)
		c.methods = []
		for m in methods:
			c.methods.append([m.idpaymentmethod,m.dtname])
		c.heading = '%s payment for user %s' % (action, c.payment.limember)

		return render('/payments/editPayment.mako')


	# I suspect keyError catching only works with forms in editPayment created by the FormBuild module
	@restrict('POST')
	@validate(schema=PaymentForm(), form='editPayment')
	def savePayment(self):
		""" Save a new or edited payment """

		if (self.form_result['idpayment'] != None):
			np = Session.query(Payment).filter(Payment.idpayment == request.params['idpayment']).one()
		else:
			np = Payment()
			# not foreseen to add recurring payments in the admin interface

		for key, value in self.form_result.items():
			setattr(np, key, value)

		if np.dtmode == 'single':
			np.dtverified = True	
			np.dtrate = np.dtamount

		Session.add(np)
		np.save() # defined in Payment model
		## how to test for success? --> if np.idpayment set
		#print(repr(np.idpayment))

		## todo: recalculate member.leavingDate

		session['flash'] = 'Payment saved successfully.'
		session.save()

		redirect(url(controller='payments', action='listPayments', member_id=self.form_result['limember']))


	@ActionProtector(has_permission('delete_payment'))
	def delete(self):
		""" Delete a payment specified by an id """
		return "I would have deleted it, honestly!"
