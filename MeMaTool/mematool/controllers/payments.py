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
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

class PaymentsController(BaseController):

    def index(self):
        return self.showOutstanding()
        
    def showOutstanding(self):
    	return render('/payments/showOutstanding.mako')
    	
    	
  	def showPayments(self):
  		if (not 'member_id' in request.params):
			redirect(url(controller='payments', action='showOutstanding'))
		
		
  		return render('/payments/showPayments.mako')
