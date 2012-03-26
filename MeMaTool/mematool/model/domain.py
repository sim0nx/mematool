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



class Domain(object):
  str_vars = ['dc']

  def __repr__(self):
    return "<Domain('dc=%s')>" % (self.dc)

  def __init__(self):
    for v in self.str_vars:
      setattr(self, v, '')

    self.all_vars = []
    self.all_vars.extend(self.str_vars)

  def __eq__(self, om):
    equal = True

    for v in self.all_vars:
      if not getattr(self, v) == getattr(om, v):
        equal = False
        break

    return equal

  def __ne__(self, om):
    return not self == om
