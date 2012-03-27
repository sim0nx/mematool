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
  def isParamStr(p, min_len=0, max_len=999999, regex=None):
    if len(p) >= min_len  and len(p) <= max_len:
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
  def _baseCheckString(fn, error_msg, param=True, **kwargs):
    if param and TypeChecker.isParamSet(fn):
      fn = request.params[fn]
    else:
      raise InvalidParameterFormat(error_msg)

    if not TypeChecker.isParamStr(fn, **kwargs):
      raise InvalidParameterFormat(error_msg)

    return True

  @staticmethod
  def checkEmail(fn, param=True):
    return ParamChecker._baseCheckString(fn, _('Invalid e-mail address'),\
      param=param, regex=regex.email)

  @staticmethod
  def checkDomain(fn, param=True):
    return ParamChecker._baseCheckString(fn, _('Invalid domain'), param=param,\
      max_len=64, regex=regex.domain)

  @staticmethod
  def checkUsername(fn, param=True):
    return ParamChecker._baseCheckString(fn, _('Invalid username'), param=param,\
      max_len=64, regex=regex.username)

  @staticmethod
  def checkString(fn, param=True, min_len=0, max_len=255, regex=None):
    return ParamChecker._baseCheckString(fn, _('Invalid value'), param=param,\
      min_len=min_len, max_len=max_len, regex=regex)

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
    return ParamChecker._baseCheckString(fn, _('Invalid phone number'),\
      param=param, regex=regex.phone)

  @staticmethod
  def checkDate(fn, param=True):
    return ParamChecker._baseCheckString(fn, _('Invalid date'),\
      param=param, regex=regex.date)

  @staticmethod
  def checkPGP(fn, param=True):
    return ParamChecker._baseCheckString(fn, _('Invalid PGP key'),\
      param=param, regex=regex.pgpKey)

  @staticmethod
  def checkiButtonUID(fn, param=True):
    return ParamChecker._baseCheckString(fn, _('Invalid iButton UID'),\
      param=param, regex=regex.iButtonUID)

  @staticmethod
  def checkPassword(fn1, fn2, param=True, min_len=8, max_len=999, regex=None):
    ParamChecker._baseCheckString(fn1, _('Invalid password'), param=param,\
      min_len=min_len, max_len=max_len, regex=regex)

    if param and TypeChecker.isParamSet(fn2):
      fn1 = request.params[fn1]
      fn2 = request.params[fn2]
    else:
      raise InvalidParameterFormat(_('Second password not valid'))

    if not fn1 == fn2:
      raise InvalidParameterFormat(_('Passwords do not match'))

    return True
