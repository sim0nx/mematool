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
from pylons.controllers.util import redirect

from mematool.model.schema.payments import PaymentForm
from mematool.lib.base import BaseController, render, Session
from mematool.lib.helpers import *
from mematool.model import Payment, Member, Paymentmethod

#from mematool.model.auth import Permission

import re
from mematool.lib.syn2cat import regex

from mematool.lib.syn2cat.ldapConnector import LdapConnector
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from webob.exc import HTTPUnauthorized
from datetime import date

# Decorators
from pylons.decorators import validate
from pylons.decorators.rest import restrict

import dateutil.parser
import datetime

import gettext
_ = gettext.gettext


class PaymentsController(BaseController):
	def __init__(self):
		super(PaymentsController, self).__init__()

	def __before__(self, action, **param):
		super(PaymentsController, self).__before__()

	def _require_auth(self):
		return True


	def index(self):
		if self.authAdapter.user_in_group('office', self.identity):
			return self.showOutstanding()

		return redirect(url(controller='payments', action='listPayments', member_id=self.identity))

	@BaseController.needAdmin
	def validatePayment(self):
		""" Validate a payment specified by an id """
		if not self._isParamStr('member_id') or not self._isParamInt('idPayment'):
			redirect(url(controller='payments', action='index'))

		try:
			np = Session.query(Payment).filter(Payment.idpayment == request.params['idPayment']).one()

			if np.dtverified:
				np.dtverified = False
			else:
				np.dtverified = True
			Session.commit()

			session['flash'] = 'Payment validation successfully toggled'
			session['flash_class'] = 'success'
		except:
			session['flash'] = 'Saving payment failed'
			session['flash_class'] = 'error'

		session.save()

		redirect(url(controller='payments', action='listPayments', member_id=request.params['member_id']))

	@BaseController.needAdmin
	def showOutstanding(self):
		""" Show which users still need to pay their membership fees and if a reminder has already been sent """

		ldapcon = LdapConnector()
		activeMembers = ldapcon.getActiveMemberList()

		#try:
		#	nummissing = Session.query(Payment).filter("dtdate<:now AND dtverified=:verified AND dtmode=:mode").params(now=date.today(),verified=0,mode='recurring').count()
		#	nummissing += 0
		#	c.heading = "%d outstanding payments" % nummissing
		#except NoResultFound:
		#	return 'No unpaid fees'
		
		# Prepare add payment form
		c.heading = 'Payments overview'
		c.members = []
		c.member_ids = []
		for uid in activeMembers:
			last_payment = None

			m = Member(uid)
			

			try:
				last_payment = Session.query(Payment).filter(and_(Payment.limember == m.uidNumber, Payment.dtverified == 1)).order_by(Payment.dtdate.desc()).limit(1)[0]
			except:
				''' Don't care if there is no payment '''
				pass

			m.paymentGood = 'no'

			if last_payment:
				d = last_payment.dtdate
				today = datetime.datetime.now().date()

				if d.year == today.year and d.month == today.month:
					m.paymentGood = 'yes'


			c.members.append(m)
			c.member_ids.append(uid)

		c.actions = list()

		return render('/payments/showOutstanding.mako')


	def listPayments(self):
		""" Show a specific user's payments """
		if (not 'member_id' in request.params):
			redirect(url(controller='payments', action='showOutstanding'))
		elif not self.isAdmin() and not request.params['member_id'] == self.identity:
			redirect(url(controller='error', action='forbidden'))


		c.heading = 'Payments for user %s' % request.params['member_id']

		## ideally, fetch monthly from member and the rest from payment (one to many relation)
		## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html
		#payment_q = Session.query(Payment).filter(Payment.limember == request.params['member_id'])

		## having problems establishing relations, thus doing a second query
		#member_q = Session.query(Member).filter(Member.idmember == request.params['member_id'])
		
		## using a join while trying to figure out how to make relations work (can't get this to work either)
		#query = Session.query(Member,Payment).filter(Payment.limember == Member.idmember).filter(Member.idmember == request.params['member_id'])

		## consider pagination
		# http://pylonsbook.com/en/1.1/starting-the-simplesite-tutorial.html#using-pagination
                try:
			#member = member_q.one()
			member = Member()
			member.uid = request.params['member_id']
			member.loadFromLdap()
			c.member = member
			c.member_id = member.uidNumber
			#c.member.leavingDate = date(int(member.leavingDate[:4]),int(member.leavingDate[5:6]),int(member.leavingDate[7:8]))
			## ideally, fetch monthly from member and the rest from payment (one to many relation)
			## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html
			payment_q = Session.query(Payment).filter(Payment.limember == member.uidNumber)


			c.payments = payment_q.all()
		
			c.unverifiedPledges = 0
			for payment in c.payments:
				if payment.dtverified == 0 and payment.dtmode == 'recurring':
					c.unverifiedPledges += 1

			## hmm this doesn't raie NoResultFound but has None as value of lastpayment
			lastpayment = payment_q.order_by(Payment.idpayment).first()

			if lastpayment:
				c.ppm = lastpayment.dtrate
			else:
				c.ppm = 0

		except AttributeError, e:
			return 'This member has made no payments o.O ?!: %s' % e
		except NoResultFound:
			return "this member has no payments on records"	## replace by "this member has made no payments" message
		    
		session['return_to'] = ('payments','listPayments')
		session.save()

		c.actions = list()
		c.actions.append( ('Add payment', 'payments', 'editPayment', request.params['member_id']) )

		return render('/payments/listPayments.mako')


	def editPayment(self):
		""" Add or edit a payment to/of a specific user """
		if not 'member_id' in request.params or request.params['member_id'] == '':
			redirect(url(controller='members', action='index'))
		elif not self.isAdmin() and not request.params['member_id'] == self.identity:
			redirect(url(controller='error', action='forbidden'))

		c.member_id = request.params['member_id']

		# vary form depending on mode (do that over ajax)
		if not 'idPayment' in request.params or request.params['idPayment'] == '0':
			c.payment = Payment()
			action = 'Adding'
		elif not request.params['idPayment'] == '' and IsInt(request.params['idPayment']) and int(request.params['idPayment']) > 0:
			action = 'Editing'
			payment_q = Session.query(Payment).filter(Payment.idpayment == int(request.params['idPayment']))
			try:
				payment = payment_q.one()
				payment.dtdate = payment.dtdate.strftime("%Y-%m-%d") #str(payment.dtdate.year) + '-' + str(payment.dtdate.month) + '-' + str(payment.dtdate.day)

				# @TODO allow member editing if not verified???
				if payment.dtverified and not self.isAdmin():
					redirect(url(controller='error', action='forbidden'))

				c.payment = payment
			except NoResultFound:
				print "oops"
				redirect(url(controller='members', action='index'))
		else:
			redirect(url(controller='members', action='index'))

		methods = Session.query(Paymentmethod).all()
		## how to easily turn a result object into a list? (more efficiently than this)
		c.methods = []
		for m in methods:
			c.methods.append([m.idpaymentmethod,m.dtname])
		c.heading = '%s payment for user %s' % (action, c.member_id)

		c.actions = list()
		c.actions.append( ('List payments', 'payments', 'listPayments', request.params['member_id']) )


		return render('/payments/editPayment.mako')


	def checkPayment(f):
		def new_f(self):
			# @TODO request.params may contain multiple values per key... test & fix
			if (not 'member_id' in request.params):
				redirect(url(controller='members', action='index'))
			elif not self.isAdmin() and not request.params['member_id'] == self.identity:
				redirect(url(controller='error', action='forbidden'))
			else:
				formok = True
				errors = []
				items = {}

				if not self._isParamFloat('dtamount', max_len=6):
					#uest.params or request.params['dtamount'] == '' or not IsInt(request.params['dtamount']) or  len(request.params['dtamount']) > 4:
					formok = False
					errors.append(_('Invalid amount'))

				if not 'dtdate' in request.params or not re.match(regex.date, request.params['dtdate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid date'))

				if not self._isParamStr('dtreason', max_len=150):
					formok = False
					errors.append(_('Malformated reason'))

				if not self._isParamInt('lipaymentmethod') or not int(request.params['lipaymentmethod']) <= 3:
					formok = False
					errors.append(_('Invalid payment method'))


				if self._isParamInt('idPayment'):
					items['idPayment'] = int(request.params['idPayment'])
				else:
					items['idPayment'] = 0


				if not formok:
					session['errors'] = errors
					session['reqparams'] = {}

					# @TODO request.params may contain multiple values per key... test & fix
					for k in request.params.iterkeys():
						session['reqparams'][k] = request.params[k]
						
					session.save()

					redirect(url(controller='payments', action='editPayment', member_id=request.params['member_id'], idPayment=items['idPayment'], mode='single'))
				else:
					items['dtamount'] = float(request.params['dtamount'])
					items['dtdate'] = request.params['dtdate']
					items['dtreason'] = request.params['dtreason']
					items['lipaymentmethod'] = request.params['lipaymentmethod']


			return f(self, request.params['member_id'], items)
		return new_f



	@checkPayment
	@restrict('POST')
	def savePayment(self, member_id, items):
		""" Save a new or edited payment """

		if items['idPayment'] > 0:
			np = Session.query(Payment).filter(Payment.idpayment == items['idPayment']).one()
		else:
			np = Payment()
			np.dtmode = 'single'
			np.dtverified = False
			# not foreseen to add recurring payments in the admin interface

		for key, value in items.iteritems():
			setattr(np, key, value)

		if np.dtmode == 'single':
			np.dtrate = np.dtamount

		ldapcon = LdapConnector()

		try:
			uidNumber = ldapcon.getUidNumberFromUid(member_id)
			np.limember = uidNumber
		except:
			session['flash'] = _('Invalid member')
			session.save()
			redirect(url(controller='payments', action='listPayments', member_id=member_id))

		# Cleanup session
		if 'reqparams' in session:
			del(session['reqparams'])
		session.save()
		##########

		Session.add(np)
		Session.commit()

		session['flash'] = 'Payment saved successfully.'
		session['flash_class'] = 'success'
		session.save()

		redirect(url(controller='payments', action='listPayments', member_id=member_id))

	@BaseController.needAdmin
	def deletePayment(self):
		""" Delete a payment specified by an id """
		if not self._isParamStr('member_id') or not self._isParamInt('idPayment'):
			redirect(url(controller='members', action='index'))

		try:
			np = Session.query(Payment).filter(Payment.idpayment == request.params['idPayment']).one()
			Session.delete(np)
			Session.commit()
		except:
			''' Don't care '''
			pass

		redirect(url(controller='payments', action='listPayments', member_id=request.params['member_id']))
