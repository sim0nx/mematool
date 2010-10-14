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

		members_q = Session.query(Member)
		members = members_q.all()
		c.members = members

		return render('/members/index.mako')


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
                def new_f(self):
                        if (not 'member_id' in request.params):
                                redirect(url(controller='members', action='showAllMembers'))
                        elif (not 'cn' in request.params or
                                not 'sn' in request.params or
                                not 'gn' in request.params or
                                not 'homeDirectory' in request.params or
                                not 'mobile' in request.params):
                                redirect(url(controller='members', action='editMember', member_id=request.params['member_id']))


			member = {'member_id':request.params['member_id'],
					'cn':request.params['cn'],
					'sn':request.params['sn'],
					'gn':request.params['gn'],
					'homeDirectory':request.params['homeDirectory'],
					'mobile':request.params['mobile']
				}


                        return f(self, member)

                return new_f


	@checkMember
	def doEditMember(self, m):
		member_q = Session.query(Member).filter(Member.dtusername == m['member_id'])

		try:
			member = member_q.one()

                        try:
                                member.loadFromLdap()

				member.cn = m['cn']
				member.sn = m['sn']
				member.gn = m['gn']
				member.homeDirectory = m['homeDirectory']
				member.mobile = m['mobile']

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
