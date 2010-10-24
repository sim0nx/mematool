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


class MembersController(BaseController):

	def __init__(self):
		self.ldapcon = LdapConnector()


	def index(self):
		return self.showAllMembers()

		#members_q = Session.query(Member)
		#members = members_q.all()
		#c.members = members
		#return render('/members/index.mako')


	def editMember(self):
		if (not 'member_id' in request.params):
			redirect(url(controller='members', action='showAllMembers'))

		member_q = Session.query(Member).filter(Member.dtusername == request.params['member_id'])

		try:
			member = member_q.one()

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
		# @TODO add more tests on the content
		# @TODO actually display errors !
                def new_f(self):
                        if (not 'member_id' in request.params):
                                redirect(url(controller='members', action='showAllMembers'))
                        elif (not 'cn' in request.params or
                                not 'sn' in request.params or
                                not 'gn' in request.params or
				not 'birthDate' in request.params or
				not 'address' in request.params or
				not 'phone' in request.params or
				not 'mobile' in request.params or
				not 'mail' in request.params or
				not 'loginShell' in request.params or
                                not 'homeDirectory' in request.params or
				not 'arrivalDate' in request.params or
				not 'leavingDate' in request.params):
                                redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))
			elif ( ('userPassword' in request.params and 'userPassword2' in request.params)
				and
				(request.params['userPassword'] != request.params['userPassword2'])):
				redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))


                        return f(self)

                return new_f


	@checkMember
	def doEditMember(self):
		member_q = Session.query(Member).filter(Member.dtusername == request.params['member_id'])

		try:
			member = member_q.one()

                        try:
                                member.loadFromLdap()

				member.cn = request.params['cn']
				member.sn = request.params['sn']
				member.gn = request.params['gn']
				member.homeDirectory = request.params['homeDirectory']
				member.mobile = request.params['mobile']
				member.birthDate = request.params['birthDate']
				member.address = request.params['address']
				member.phone = request.params['phone']
				member.mail = request.params['mail']
				member.loginShell = request.params['loginShell']
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

				redirect(url(controller='members', action='showAllMembers'))

                        except LookupError:
                                print 'No such ldap user !'

                except NoResultFound:
                        print 'No such sql user !'


	def showAllMembers(self):
		members_q = Session.query(Member)

		try:
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
