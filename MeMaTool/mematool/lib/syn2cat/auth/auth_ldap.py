# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2011, Georges Toth <georges@trypill.org>.
# All Rights Reserved.
#
##############################################################################

"""The groups and permission adapters for LDAP sources"""


from mematool.lib.syn2cat.ldapConnector import LdapConnector



class LDAPAuthAdapter(object):
    """The base class for LDAP source adapters"""
    
    def __init__(self, **kwargs):
        self.baseDN = 'dc=hackerspace,dc=lu'
	self.userDN = 'ou=People,' + self.baseDN
	self.groupDN = 'ou=Group,' + self.baseDN
	self.ldapcon = LdapConnector()
	self.con = self.ldapcon.getLdapConnection()
        super(LDAPAuthAdapter, self).__init__(**kwargs)

    
    def get_all_groups(self):
        sections = ['office', 'sysops', 'syn2cat_full_member']

        return sections

    
    def user_in_group(self, group, user):
	group_members = self.ldapcon.getGroupMembers(group)

	if user in group_members:
		return True

	return False
    

    def group_exists(self, group):
	groups = self._get_all_groups()

	if group in groups:
		return True

	return False
