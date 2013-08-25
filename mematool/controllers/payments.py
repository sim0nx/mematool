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
from cherrypy._cperror import HTTPRedirect, HTTPError
import logging
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_, or_
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
from mematool.controllers import BaseController, TemplateContext
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.lechecker import ParamChecker
from mematool.model.dbmodel import Payment

log = logging.getLogger(__name__)


# @todo remove this
def IsInt(string):
  try:
    num = int(string)
  except ValueError as e:
    return False

  return True


class PaymentsController(BaseController):
  _cp_config = {'tools.require_auth.on': True}

  def __init__(self):
    super(PaymentsController, self).__init__()

  def _sidebar(self):
    self.sidebar = []
    self.sidebar.append({'name': _('All payments'), 'args': {'controller': 'payments', 'action': 'listPayments'}})
    self.sidebar.append({'name': _('Outstanding payment'), 'args': {'controller': 'payments', 'action': 'index'}})

  @cherrypy.expose()
  def index(self):
    if self.is_admin() or self.mf.isUserInGroup(self.session.get('username'), 'office'):
      return self.showOutstanding()

    raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(self.session.get('username')))

  @cherrypy.expose()
  @BaseController.needFinanceAdmin
  def validatePayment(self, member_id, idPayment):
    """ Validate a payment specified by an id """
    try:
      ParamChecker.checkUsername('member_id', param=True)
      ParamChecker.checkInt('idPayment', param=True)
    except:
      raise HTTPRedirect('/payments/index')

    try:
      np = self.db.query(Payment).filter(Payment.id == idPayment).one()

      if np.verified:
        np.verified = False
      else:
        np.verified = True
      self.request.db.commit()

      self.session['flash'] = _('Payment validation successfully toggled')
      self.session['flash_class'] = 'success'
    except:
      self.session['flash'] = _('Saving payment failed')
      self.session['flash_class'] = 'error'

    self.session.save()

    raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(member_id))

  def _getLastPayment(self, uid):
    member = self.mf.getUser(uid)
    lastDate = parser.parse(member.arrivalDate)

    try:
      p = self.db.query(Payment).filter(and_(Payment.uid == uid, or_(Payment.status == 0, Payment.status == 2))).order_by(Payment.date.desc()).first()
      lastDate = p.date + relativedelta(months=+ 1)
    except Exception as e:
      pass

    return lastDate

  @cherrypy.expose()
  def bulkAdd(self, member_id):
    try:
      ParamChecker.checkUsername('member_id', param=True)
    except:
      raise HTTPRedirect('/payments/index')

    c = TemplateContext()
    c.member_id = member_id
    c.heading = _('Add bulk payments')

    return self.render('/payments/bulkAdd.mako', template_context=c)

  @cherrypy.expose()
  def doBulkAdd(self, member_id, months, verified=None):
    try:
      ParamChecker.checkUsername('member_id', param=True)
      ParamChecker.checkInt('months', param=True, max_len=2)
    except:
      raise HTTPRedirect('/payments/index')

    lastDate = self._getLastPayment(member_id)
    months = int(months)

    if self.is_finance_admin():
      try:
        ParamChecker.checkInt('verified', param=True, max_len=1)
        verified = True
      except:
        verified = False

    try:
      for i in range(months):
        p = Payment()
        p.uid = member_id
        p.date = lastDate + relativedelta(months=i)
        p.status = 0
        p.verified = verified

        self.db.add(p)

      self.db.commit()

      self.session['flash'] = _('Payments added')
      self.session['flash_class'] = 'success'
    except Exception as e:
      self.session['flash'] = _('Operation failed')
      self.session['flash_class'] = 'error'

    self.session.save()

    raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(member_id))

  @cherrypy.expose()
  @BaseController.needAdmin
  def showOutstanding(self, showAll=0):
    """ Show which users still need to pay their membership fees and if a reminder has already been sent """
    if showAll == '1':
      showAll = True
    else:
      showAll = False

    activeMembers = self.mf.getActiveMemberList()

    # Prepare add payment form
    c = TemplateContext()
    c.heading = _('Outstanding payments')
    c.members = []
    c.member_ids = []
    for uid in activeMembers:
      last_payment = None

      try:
        last_payment = self.db.query(Payment).filter(and_(Payment.uid == uid, Payment.verified == 1)).order_by(Payment.date.desc()).limit(1)[0]
      except:
        ''' Don't care if there is no payment '''
        pass

      m = self.mf.getUser(uid)
      m.paymentGood = False

      if last_payment:
        d = last_payment.date
        today = datetime.datetime.now().date()

        if d.year > today.year or (d.year == today.year and d.month >= today.month):
          m.paymentGood = True

      if not m.paymentGood or showAll:
        c.members.append(m)

      c.member_ids.append(uid)

    return self.render('/payments/showOutstanding.mako', template_context=c)

  @cherrypy.expose()
  def listPayments(self, member_id=None, year=None):
    """ Show a specific user's payments """
    if member_id is None:
      if not self.is_admin() and not self.is_finance_admin():
        raise HTTPError(403, 'Forbidden')
      else:
        raise HTTPRedirect('/payments/showOutstanding/?showAll=1')
    elif not self.is_admin() and not self.is_finance_admin() and not member_id == self.session.get('username'):
      raise HTTPError(403, 'Forbidden')

    if not year is None:
      try:
        ParamChecker.checkInt('year', param=True, max_len=4)
        if int(year) > 1970 and int(year) < 2222:
          year = int(year)
        else:
          year = datetime.datetime.now().year
      except:
        pass

    if year is None:
      try:
        ParamChecker.checkUsername('member_id', param=True)
        year = self._getLastPayment(member_id).year
      except:
        pass

    if year is None:
      year = datetime.datetime.now().year

    c = TemplateContext()
    c.heading = _('Payments for the year {0}, user {1}'.format(year, member_id))
    c.member_id = member_id

    ## consider pagination
    # http://pylonsbook.com/en/1.1/starting-the-simplesite-tutorial.html#using-pagination
    try:
      #c.member.leavingDate = date(int(member.leavingDate[:4]),int(member.leavingDate[5:6]),int(member.leavingDate[7:8]))
      ## ideally, fetch monthly from member and the rest from payment (one to many relation)
      ## http://www.sqlalchemy.org/docs/05/reference/ext/declarative.html

      y_start = datetime.date(year, 1, 1)
      y_end = datetime.date(year, 12, 31)
      payment_sql = self.db.query(Payment).filter(Payment.uid == member_id).filter(Payment.date.between(y_start, y_end)).order_by(Payment.date.desc()).all()

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
      return "this member has no payments on records"  # replace by "this member has made no payments" message

    self.session['return_to'] = ('payments', 'listPayments')
    self.session.save()

    self.sidebar.append({'name': _('Add payment'), 'args': {'controller': 'payments', 'action': 'editPayment', 'params': {'member_id': member_id}}})

    return self.render('/payments/listPayments.mako', template_context=c)

  @cherrypy.expose()
  def editPayment(self, member_id, year=None, month=None, idPayment='0'):
    """ Add or edit a payment to/of a specific user """
    if not self.is_admin() and not member_id == self.session.get('username'):
      raise HTTPError(403, 'Forbidden')

    c = TemplateContext()
    c.member_id = member_id
    c.status_0 = False
    c.status_1 = False
    c.status_2 = False

    # vary form depending on mode (do that over ajax)
    if idPayment == '0':
      c.payment = Payment()
      action = 'Adding'

      try:
        ParamChecker.checkYear('year', param=True)
        ParamChecker.checkMonth('month', param=True)
        c.date = str(datetime.date(int(year), int(month), 1))
      except:
        '''Don't care ... just let the user enter a new date'''
        pass

    elif not idPayment == '' and IsInt(idPayment) and int(idPayment) > 0:
      # @fixme convert IsInt to new class
      action = 'Editing'
      payment_q = self.db.query(Payment).filter(Payment.id == int(idPayment))
      try:
        payment = payment_q.one()

        # @TODO allow member editing if not verified???
        if payment.verified and not self.is_admin():
          raise HTTPError(403, 'Forbidden')

        c.payment = payment
        setattr(c, 'status_' + str(payment.status), True)
      except NoResultFound:
        print "oops"
        raise HTTPRedirect('/members/index')
    else:
      raise HTTPRedirect('/members/index')

    c.heading = _('%s payment for user %s') % (action, c.member_id)
    self.sidebar.append({'name': _('List payments'), 'args': {'controller': 'payments', 'action': 'listPayments', 'params': {'member_id': member_id}}})

    return self.render('/payments/editPayment.mako', template_context=c)

  def checkPayment(f):
    def new_f(self, member_id, idPayment, date, status):
      # @TODO request.params may contain multiple values per key... test & fix
      if not self.is_admin() and not member_id == self.session.get('username') or (member_id == self.session.get('username') and ParamChecker.checkInt('idPayment', param=True, optional=True)):
        print 'checkPayment err0r::', str(self.isAdmin()), str(member_id), str(self.session.get('username')), str(ParamChecker.checkInt('idPayment', param=True, optional=True))
        raise HTTPError(403, 'Forbidden')
      else:
        formok = True
        errors = []
        items = {}
        d = None

        try:
          ParamChecker.checkDate('date', param=True)
          d = parser.parse(date)
          d = datetime.date(d.year, d.month, 1)
        except Exception as e:
          print e
          formok = False
          errors.append(_('Invalid date'))

        try:
          ParamChecker.checkInt('status', param=True)
          items['status'] = int(status)
        except:
          formok = False
          errors.append(_('Invalid payment status'))

        try:
          ParamChecker.checkInt('idPayment', param=True)
          items['idPayment'] = int(idPayment)
        except:
          items['idPayment'] = 0

        if not d is None and items['idPayment'] == 0:
          p_count = self.db.query(Payment).filter(Payment.uid == member_id).filter(Payment.date == d).count()

          if p_count > 0:
            formok = False
            errors.append(_('That month is already on records!'))

        if not formok:
          self.session['errors'] = errors
          self.session['reqparams'] = {}

          # @TODO request.params may contain multiple values per key... test & fix
          for k in self.request.params.iterkeys():
            self.session['reqparams'][k] = self.request.params[k]

          self.session.save()

          raise HTTPRedirect('/payments/editPayment/?member_id={0}&idPayment={1}'.format(member_id, items['idPayment']))
        else:
          items['date'] = d

      return f(self, member_id, items)
    return new_f

  @cherrypy.expose()
  @cherrypy.tools.allow(methods=['POST'])
  @checkPayment
  def savePayment(self, member_id, items):
    """ Save a new or edited payment """
    verified = False

    if self.is_finance_admin() and ParamChecker.checkInt('verified', param=True, optional=True):
      verified = True

    if items['idPayment'] > 0:
      try:
        np = self.db.query(Payment).filter(Payment.id == items['idPayment']).one()
        np.verified = verified
      except:
        self.session['flash'] = _('Invalid record')
        self.session.save()
        raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(member_id))
    else:
      np = Payment()
      np.verified = verified
      np.status = 0

    for key, value in items.iteritems():
      setattr(np, key, value)

    try:
      np.uid = member_id
    except:
      self.session['flash'] = _('Invalid member')
      self.session.save()
      raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(member_id))

    # Cleanup session
    if 'reqparams' in self.session:
      del(self.session['reqparams'])
    self.session.save()
    ##########

    self.db.add(np)
    self.db.commit()

    self.session['flash'] = _('Payment saved successfully.')
    self.session['flash_class'] = 'success'
    self.session.save()

    raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(member_id))

  @cherrypy.expose()
  @BaseController.needFinanceAdmin
  def deletePayment(self, member_id, idPayment):
    """ Delete a payment specified by an id """
    try:
      ParamChecker.checkUsername('member_id', param=True)
      ParamChecker.checkInt('idPayment', param=True)
    except:
      raise HTTPRedirect('/members/index')

    try:
      np = self.db.query(Payment).filter(Payment.id == idPayment).one()
      self.db.delete(np)
      self.db.commit()
    except:
      ''' Don't care '''
      pass

    raise HTTPRedirect('/payments/listPayments/?member_id={0}'.format(member_id))
