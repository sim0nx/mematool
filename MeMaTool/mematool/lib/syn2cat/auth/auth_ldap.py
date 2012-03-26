# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2011, Georges Toth <georges@trypill.org>.
# All Rights Reserved.
#
##############################################################################

"""The groups and permission adapters for LDAP sources"""


from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import redirect

from mematool.lib.syn2cat.ldapConnector import LdapConnector


class LDAPAuthAdapter(object):
  """The base class for LDAP source adapters"""
  
  def __init__(self, **kwargs):
    super(LDAPAuthAdapter, self).__init__(**kwargs)

  def authenticate(self, username, password):
    """Authenticate a user via LDAP and return his/her LDAP properties.

     Raises AuthenticationError if the credentials are rejected, or
     EnvironmentError if the LDAP server can't be reached.
     """

    try:
      ldapcon = LdapConnector(uid=username, password=password)

      return True
    except:
      return False
