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

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from mematool.lib.base import BaseController, render, Session
from mematool.lib.helpers import *
from mematool.model import Payment, Member, Paymentmethod

#from mematool.model.auth import Permission

import re
from mematool.lib.syn2cat import regex

from mematool.model.ldapModelFactory import LdapModelFactory
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from webob.exc import HTTPUnauthorized
from datetime import date, datetime
from dateutil import parser

# Decorators
from pylons.decorators import validate
from pylons.decorators.rest import restrict

import gettext
_ = gettext.gettext


class PaymentsController(BaseController):
	def __init__(self):
		super(PaymentsController, self).__init__()
		self.lmf = LdapModelFactory()

		c.actions = list()
		c.actions.append( (_('All payments'), 'payments', 'listPayments') )
		c.actions.append( (_('Outstanding payment'), 'payments', 'index') )

	def __before__(self, action, **param):
		super(PaymentsController, self).__before__()

	def _require_auth(self):
		return True

	def index(self):
		if self.lmf.isUserInGroup(self.identity, 'office'):
			return self.showOutstanding()

		return redirect(url(controller='payments', action='listPayments', member_id=self.identity))

	@BaseController.needFinanceAdmin
	def validatePayment(self):
		""" Validate a payment specified by an id """
		if not self._isParamStr('member_id') or not self._isParamInt('idPayment'):
			redirect(url(controller='payments', action='index'))

		try:
			np = Session.query(Payment).filter(Payment.id == request.params['idPayment']).one()

			if np.verified:
				np.verified = False
			else:
				np.verified = True
			Session.commit()

			session['flash'] = _('Payment validation successfully toggled')
			session['flash_class'] = 'success'
		except:
			session['flash'] = _('Saving payment failed')
			session['flash_class'] = 'error'

		session.save()

		redirect(url(controller='payments', action='listPayments', member_id=request.params['member_id']))

	@BaseController.needFinanceAdmin
	def duplicatePayment(self):
		if not self._isParamStr('member_id') or not self._isParamInt('idPayment'):
			redirect(url(controller='payments', action='index'))

		npID = -1

		try:
			p = Session.query(Payment).filter(Payment.idpayment == request.params['idPayment']).one()

			np = Payment()
			np.uid = p.uid
			np.date = datetime.now().date()
			np.status = p.status
			np.verified = False

			Session.add(np)
			Session.commit()

			npID = np.idpayment

			session['flash'] = _('Payment duplicated')
			session['flash_class'] = 'success'
		except:
			session['flash'] = _('Duplication failed')
			session['flash_class'] = 'error'

		session.save()

		redirect(url(controller='payments', action='editPayment', member_id=request.params['member_id'], idPayment=npID))

	@BaseController.needAdmin
	def showOutstanding(self):
		""" Show which users still need to pay their membership fees and if a reminder has already been sent """

		showAll = False
		if 'showAll' in request.params and request.params['showAll'] == '1':
			showAll = True

		activeMembers = self.lmf.getActiveMemberList()

		# Prepare add payment form
		c.heading = _('Outstanding payments')
		c.members = []
		c.member_ids = []
		for uid in activeMembers:
			last_payment = None

			try:
				last_payment = Session.query(Payment).filter(and_(Payment.uid == uid, Payment.verified == 1)).order_by(Payment.date.desc()).limit(1)[0]
			except:
				''' Don't care if there is no payment '''
				pass

			m = self.lmf.getUser(uid)
			m.paymentGood = False

			if last_payment:
				d = last_payment.date
				today = datetime.now().date()

				if d.year > today.year or (d.year == today.year and d.month >= today.month):
					m.paymentGood = True

			if not m.paymentGood or showAll:
				c.members.append(m)

			c.member_ids.append(uid)

		return render('/payments/showOutstanding.mako')

	def listPayments(self):
		""" Show a specific user's payments """
		if (not 'member_id' in request.params):
			if not self.isAdmin() and not self.isFinanceAdmin():
				redirect(url(controller='error', action='forbidden'))
			else:
				redirect(url(controller='payments', action='showOutstanding', showAll='1'))
		elif not self.isAdmin() and not self.isFinanceAdmin() and not request.params['member_id'] == self.identity:
			redirect(url(controller='error', action='forbidden'))

		year = datetime.now().year
		if 'year' in request.params and IsInt(request.params['year']) and int(request.params['year']) > 1970 and int(request.params['year']) < 2222:
			year = int(request.params['year'])

		c.heading = _('Payments for the year %s, user %s') % (str(year), request.params['member_id'])
		c.member_id = request.params['member_id']

		## consider pagination
		# http://pylonsbook.com/en/1.1/starting-the-simplesite-tutorial.html#using-pagination
                try:
			#c.member.leavingDate = date(int(member.leavingDate[:4]),int(member.leavingDate[5:6]),int(member.leavingDate[7:8]))
			## ideally, fetch monthly from member and the rest from payment (one to many relation)
			## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html

			y_start = date(year, 1, 1)
			y_end = date(year, 12, 31)
			payment_sql = Session.query(Payment).filter(Payment.uid == request.params['member_id']).filter(Payment.date.between(y_start, y_end)).order_by(Payment.date.desc()).all()

			payments = {}
			c.unverifiedPledges = 0
			for p in payment_sql:
				if p.verified == 0:
					c.unverifiedPledges += 1
				payments[p.date.month] = p

			c.year = year
			c.payments = payments
		

		except AttributeError, e:
			return 'This member has made no payments o.O ?!: %s' % e
		except NoResultFound:
			return "this member has no payments on records"	## replace by "this member has made no payments" message
		    
		session['return_to'] = ('payments','listPayments')
		session.save()

		# blind call ... we don't care about the return value
		# but only that the call sets a session variable
		self.isFinanceAdmin()

		c.actions.append( ('Add payment', 'payments', 'editPayment', request.params['member_id']) )

		return render('/payments/listPayments.mako')

	def editPayment(self):
		""" Add or edit a payment to/of a specific user """
		if not 'member_id' in request.params or request.params['member_id'] == '':
			redirect(url(controller='members', action='index'))
		elif not self.isAdmin() and not request.params['member_id'] == self.identity:
			redirect(url(controller='error', action='forbidden'))

		c.member_id = request.params['member_id']
		c.status_0 = False
		c.status_1 = False
		c.status_2 = False

		# vary form depending on mode (do that over ajax)
		if not 'idPayment' in request.params or request.params['idPayment'] == '0':
			c.payment = Payment()
			action = 'Adding'

			if 'year' in request.params and 'month' in request.params and\
				IsInt(request.params['year']) and int(request.params['year']) > 1970 and int(request.params['year']) < 2222 and\
				IsInt(request.params['month']) and int(request.params['month']) >= 1 and int(request.params['month']) <= 12:
				c.date = str(date(int(request.params['year']), int(request.params['month']), 1))

		elif not request.params['idPayment'] == '' and IsInt(request.params['idPayment']) and int(request.params['idPayment']) > 0:
			action = 'Editing'
			payment_q = Session.query(Payment).filter(Payment.id == int(request.params['idPayment']))
			try:
				payment = payment_q.one()
				payment.date = payment.date.strftime("%Y-%m-%d")

				# @TODO allow member editing if not verified???
				if payment.verified and not self.isAdmin():
					redirect(url(controller='error', action='forbidden'))

				c.payment = payment
				setattr(c, 'status_' + str(payment.status), True)
			except NoResultFound:
				print "oops"
				redirect(url(controller='members', action='index'))
		else:
			redirect(url(controller='members', action='index'))

		c.heading = _('%s payment for user %s') % (action, c.member_id)

		c.actions.append( ('List payments', 'payments', 'listPayments', request.params['member_id']) )

		return render('/payments/editPayment.mako')

	def checkPayment(f):
		def new_f(self):
			# @TODO request.params may contain multiple values per key... test & fix
			if (not 'member_id' in request.params):
				redirect(url(controller='members', action='index'))
			elif not self.isAdmin() and not request.params['member_id'] == self.identity or (request.params['member_id'] == self.identity and self._isParamInt('idPayment')):
				redirect(url(controller='error', action='forbidden'))
			else:
				formok = True
				errors = []
				items = {}
				d = None

				if not 'date' in request.params or not re.match(regex.date, request.params['date'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid date'))
				else:
					d = parser.parse(request.params['date'])
					d = date(d.year, d.month, 1)

				if not 'status' in request.params or not self._isParamInt('status'):
					formok = False
					errors.append(_('Invalid payment status'))
					print request.params['status']
				else:
					items['status'] = int(request.params['status'])

				if self._isParamInt('idPayment'):
					items['idPayment'] = int(request.params['idPayment'])
				else:
					items['idPayment'] = 0

				if not d is None and items['idPayment'] == 0:
					p_count = Session.query(Payment).filter(Payment.uid == request.params['member_id']).filter(Payment.date == d).count()

					if p_count > 0:
						formok = False
						errors.append(_('That month is already on records!'))

				if not formok:
					session['errors'] = errors
					session['reqparams'] = {}

					# @TODO request.params may contain multiple values per key... test & fix
					for k in request.params.iterkeys():
						session['reqparams'][k] = request.params[k]
						
					session.save()

					redirect(url(controller='payments', action='editPayment', member_id=request.params['member_id'], idPayment=items['idPayment']))
				else:
					items['date'] = d


			return f(self, request.params['member_id'], items)
		return new_f

	@checkPayment
	@restrict('POST')
	def savePayment(self, member_id, items):
		""" Save a new or edited payment """

		if items['idPayment'] > 0:
			try:
				np = Session.query(Payment).filter(Payment.id == items['idPayment']).one()
			except:
				session['flash'] = _('Invalid record')
				session.save()
				redirect(url(controller='payments', action='listPayments', member_id=member_id))
		else:
			np = Payment()
			np.verified = False
			np.status = 0

		for key, value in items.iteritems():
			setattr(np, key, value)

		try:
			np.uid = member_id
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

		session['flash'] = _('Payment saved successfully.')
		session['flash_class'] = 'success'
		session.save()

		redirect(url(controller='payments', action='listPayments', member_id=member_id))

	@BaseController.needFinanceAdmin
	def deletePayment(self):
		""" Delete a payment specified by an id """
		if not self._isParamStr('member_id') or not self._isParamInt('idPayment'):
			redirect(url(controller='members', action='index'))

		try:
			np = Session.query(Payment).filter(Payment.id == request.params['idPayment']).one()
			Session.delete(np)
			Session.commit()
		except:
			''' Don't care '''
			pass

		redirect(url(controller='payments', action='listPayments', member_id=request.params['member_id']))
