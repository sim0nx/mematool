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
from mematool.model import Member

log = logging.getLogger(__name__)

from mematool.lib.syn2cat.ldapConnector import LdapConnector
from sqlalchemy.orm.exc import NoResultFound
import re
from mematool.lib.syn2cat import regex

from webob.exc import HTTPUnauthorized

import gettext
_ = gettext.gettext



class MembersController(BaseController):

	def __init__(self):
		self.ldapcon = LdapConnector()


	def __before__(self):
                if self.identity is None:
			raise HTTPUnauthorized()


	def index(self):
		return self.showAllMembers()


	def editMember(self):
		if (not 'member_id' in request.params):
			redirect(url(controller='members', action='showAllMembers'))

		member_q = Session.query(Member).filter(Member.idmember == request.params['member_id'])

		try:
			member = member_q.one()

			c.heading = 'Edit member'

			try:
				member.loadFromLdap()

				c.member = member

				return render('/members/editMember.mako')

			except LookupError:
				print 'No such ldap user !'

		except NoResultFound:
			print 'No such sql user !'


		return 'ERROR 4x0'


        def checkMember(f):
                def new_f(self):
			# @TODO request.params may contain multiple values per key... test & fix
                        if (not 'member_id' in request.params):
				redirect(url(controller='members', action='showAllMembers'))
                        else:
				formok = True
				errors = []

				if not 'cn' in request.params or request.params['cn'] == '' or len(request.params['cn']) > 40:
					formok = False
					errors.append(_('Invalid common name'))

				if not 'sn' in request.params or request.params['sn'] == '' or len(request.params['sn']) > 20:
					formok = False
					errors.append(_('Invalid surname'))

				if not 'gn' in request.params or request.params['gn'] == '' or len(request.params['gn']) > 20:
					formok = False
					errors.append(_('Invalid given name'))

				if not 'birthDate' in request.params or not re.match(regex.date, request.params['birthDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid birth date'))

				if not 'address' in request.params or request.params['address'] == '' or len(request.params['address']) > 100:
					formok = False
					errors.append(_('Invalid address'))

				if 'phone' in request.params and request.params['phone'] != '' and not re.match(regex.phone, request.params['phone'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid phone number'))

				if not 'mobile' in request.params or not re.match(regex.phone, request.params['mobile'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid mobile number'))

				if not 'mail' in request.params or not re.match(regex.email, request.params['mail'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid e-mail address'))

				if not 'loginShell' in request.params or not re.match(regex.loginShell, request.params['loginShell'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid login shell'))

				if not 'homeDirectory' in request.params or not re.match(regex.homeDirectory, request.params['homeDirectory'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid home directory'))

				if not 'arrivalDate' in request.params or not re.match(regex.date, request.params['arrivalDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid "member since" date'))

				if 'leavingDate' in request.params and request.params['leavingDate'] != '' and not re.match(regex.date, request.params['leavingDate'], re.IGNORECASE):
					formok = False
					errors.append(_('Invalid "membership canceled" date'))

				if 'userPassword' in request.params and 'userPassword2' in request.params:
					if request.params['userPassword'] != request.params['userPassword2']:
						formok = False
						errors.append(_('Passwords don\'t match'))
					elif len(request.params['userPassword']) > 0 and len(request.params['userPassword']) <= 6:
						formok = False
						errors.append(_('Password too short'))

				if not formok:
					session['errors'] = errors
					session['reqparams'] = {}

					# @TODO request.params may contain multiple values per key... test & fix
					for k in request.params.iterkeys():
						session['reqparams'][k] = request.params[k]
						
					session.save()

					redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))


                        return f(self)

                return new_f


	@checkMember
	def doEditMember(self):
		member_q = Session.query(Member).filter(Member.idmember == request.params['member_id'])

		try:
			member = member_q.one()

                        try:
				member.loadFromLdap()

				member.gidNumber = request.params['gidNumber']
				member.cn = request.params['cn']
				member.sn = request.params['sn']
				member.gn = request.params['gn']
				member.birthDate = request.params['birthDate']
				member.address = request.params['address']
				member.phone = request.params['phone']
				member.mobile = request.params['mobile']
				member.mail = request.params['mail']
				member.loginShell = request.params['loginShell']
				member.homeDirectory = request.params['homeDirectory']
				member.arrivalDate = request.params['arrivalDate']
				member.leavingDate = request.params['leavingDate']

				if 'sshPublicKey' in request.params and request.params['sshPublicKey'] != '':
					# @TODO don't blindly save it
					member.sshPublicKey = request.params['sshPublicKey']
				elif 'sshPublicKey' in vars(member):
					member.sshPublicKey = 'removed'

				if 'userPassword' in request.params and request.params['userPassword'] != '':
					member.setPassword(request.params['userPassword'])

				member.save()

				session['flash'] = 'Member details successfully edited'
				session.save()

				redirect(url(controller='members', action='showAllMembers'))

                        except LookupError:
				print 'No such ldap user !'

                except NoResultFound:
                        print 'No such sql user !'


	def showAllMembers(self):
		members_q = Session.query(Member)

		try:
			c.heading = 'All members'
			members = members_q.all()

			for m in members:
				try:
					m.loadFromLdap()
				except LookupError:
					pass

			c.members = members

			return render('/members/viewAll.mako')

		except NoResultFound:
			print 'No such sql user !'



		return 'ERROR 4x0'
