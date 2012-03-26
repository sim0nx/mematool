#
#    MeMaTool (c) 2012 Georges Toth <georges _at_ trypill _dot_ org>
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

from pylons import request
import re
from mematool.lib.syn2cat import regex
import gettext
_ = gettext.gettext


class InvalidParameterFormat(Exception):
  pass


class TypeChecker(object):
  @staticmethod
  def isInt(string):
    try:
      num = int(string)
    except ValueError as e:
      return False

    return True

  @staticmethod
  def isFloat(string):
    try:
      num = float(string)
    except ValueError as e:
      return False

    return True

  @staticmethod
  def isParamSet(p):
    if p in request.params and request.params[p] != '':
      return True

    return False

  @staticmethod
  def isParamStr(p, min_len=0, max_len=255, regex=None):
    if len(p) > min_len  and len(p) <= max_len:
      if regex != None:
        if re.match(regex, p, re.IGNORECASE):
          return True
      else:
        return True

    return False

  @staticmethod
  def isParamInt(p, min_val=0, min_len=0, max_len=4):
    if TypeChecker.isParamStr(p, min_len, max_len) and TypeChecker.isInt(p) and int(p) >= min_val:
      return True

    return False

  @staticmethod
  def isParamFloat(p, min_val=0, min_len=0, max_len=4):
    if TypeChecker.isParamStr(p, min_len, max_len) and TypeChecker.isFloat(p) and float(p) >= min_val:
      return True

    return False


class ParamChecker(object):
  @staticmethod
  def checkEmail(fn, param=True):
    error_msg = _('Invalid e-mail address')

    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    if not TypeChecker.isParamStr(fn, regex=regex.email):
      raise InvalidParameterFormat(error_msg)

    return True

  @staticmethod
  def checkDomain(fn, param=True):
    error_msg = _('Invalid domain')

    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    if not TypeChecker.isParamStr(fn, max_len=64, regex=regex.domain):
      raise InvalidParameterFormat(error_msg)

    return True

  @staticmethod
  def checkString(fn, param=True, min_len=0, max_len=255, regex=None):
    error_msg = _('Invalid value')

    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    if not TypeChecker.isParamStr(fn, min_len=min_len, max_len=max_len, regex=regex):
      raise InvalidParameterFormat(error_msg)

    return True

  @staticmethod
  def checkMode(fn, param=True, values=[]):
    error_msg = _('Invalid mode')

    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    found = False
    for v in values:
      if fn == v:
        found = True
        break

    if not found:
      raise InvalidParameterFormat(error_msg)

    return True

  @staticmethod
  def checkPhone(fn, param=True):
    error_msg = _('Invalid phone number')

    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    if not TypeChecker.isParamStr(fn, regex=regex.phone):
      raise InvalidParameterFormat(error_msg)

    return True

  @staticmethod
  def checkDate(fn, param=True):
    error_msg = _('Invalid date')

    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    if not TypeChecker.isParamStr(fn, regex=regex.date):
      raise InvalidParameterFormat(error_msg)

    return True

