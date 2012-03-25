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



class Alias(object):
	str_vars = ['dn_mail']
	list_vars = ['mail', 'maildrop']

	def __repr__(self):
		return "<Alias('dn_mail=%s')>" % (self.dn_mail)

	def __init__(self):
		for v in self.str_vars:
			setattr(self, v, '')
		for v in self.list_vars:
			setattr(self, v, [])

		self.all_vars = []
		self.all_vars.extend(self.str_vars)
		self.all_vars.extend(self.list_vars)

	def __eq__(self, om):
		equal = True

		if om is None:
			return False

		for v in self.all_vars:
			if not getattr(self, v) == getattr(om, v):
				equal = False
				break

		return equal

	def __ne__(self, om):
		return not self == om

	@property
	def domain(self):
		if not self.dn_mail == '':
			return self.dn_mail.split('@')[1]

		return None

	def getDN(self, basedn):
		if not self.dn_mail == '':
			return 'mail=' + self.dn_mail + ',dc=' + self.domain + ',' + basedn

		raise Exception('Uninitialized object')
