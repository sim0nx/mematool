# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Georges Toth <georges _at_ trypill _dot_ org>
#
# This file is part of MeMaTool.
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MeMaTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-


from pylons.i18n.translation import _

from mematool.lib.base import Session
from mematool.model import TmpMember

import urllib
import hashlib
import base64
from binascii import b2a_base64
from mematool.lib.syn2cat import regex
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat
import os


class Member():
  # ldap
  str_vars = ['uid',
    'cn',
    'sn',
    'givenName',
    'homePhone',
    'mobile',
    'mail',
    'xmppID',
    'userPassword',
    'sambaNTPassword',
    'sambaSID',
    'sshPublicKey',
    'pgpKey',
    'iButtonUID',
    'conventionSigner',
    'uidNumber',
    'gidNumber',
    'loginShell',
    'hDirectory',
    'homePostalAddress',
    'arrivalDate',
    'leavingDate',
    'nationality']
  list_vars = ['groups']
  bool_vars = ['fullMember',
    'lockedMember',
    'spaceKey',
    'npoMember',
    'isMinor']
  bin_vars = ['jpegPhoto']

  '''
  uid = ''   # uid
  cn = '' # fullname
  sn = '' # family name
  givenName = ''  # given name
  homePhone = '' # phone (homePhone)
  mobile = '' # mobile
  mail = '' # mail
  xmppID = '' # xmppID
  userPassword = '' # SSHA password
  sambaNTPassword = '' # NT Password
  sambaSID = ''
  sshPublicKey = '' # SSH public key
  pgpKey = '' # PGP key
  iButtonUID = '' # iButton UID
  conventionSigner = '' # Member convention signer
  uidNumber = '' # user id (uidNumber)
  gidNumber = '' # group id (gidNumber)
  loginShell = '' # login shell
  homeDirectory = '' # homeDirectory
  homePostalAddress = '' # homePostalAddress
  arrivalDate = '' # member since
  leavingDate = '' # membership canceled
  groups = [] # additional user groups
  fullMember = False
  lockedMember = False
  isMinor = False
  '''

  def __init__(self):
    for v in self.str_vars:
      setattr(self, v, '')
    for v in self.list_vars:
      setattr(self, v, [])
    for v in self.bool_vars:
      setattr(self, v, False)
    for v in self.bin_vars:
      setattr(self, v, None)

    self.all_vars = []
    self.all_vars.extend(self.str_vars)
    self.all_vars.extend(self.list_vars)
    self.all_vars.extend(self.bool_vars)
    self.all_vars.extend(self.bin_vars)

  def __str__(self):
    return "<Member('uidNumber=%s, uid=%s, validate=%s')>" % (self.uidNumber, self.uid, self.validate)

  def __eq__(self, om):
    equal = True

    for v in self.all_vars:
      if not getattr(self, v) == getattr(om, v):
        equal = False
        break

    return equal

  def __ne__(self, om):
    return not self == om

  @property
  def validate(self):
    if not self.uidNumber == '':
      if Session.query(TmpMember).filter(TmpMember.id == self.uidNumber).count() > 0:
        return True

    return False

  @property
  def gn(self):
    return self.givenName

  def setPassword(self, password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    self.userPassword = '{SSHA}' + b2a_base64(h.digest() + salt)[:-1]
    self.sambaNTPassword = hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()

  def generateUserSID(self):
    #@TODO put in config file
    serverSambaSID = 'S-1-1-1'
    self.sambaSID = serverSambaSID + '-' + str((int(self.uidNumber) * 2) + 1000)

  ####################
  # checker interface
  def check(self):
    errors = []
    checkOK = True

    try:
      ParamChecker.checkUsername(self.uid, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid username'))

    try:
      ParamChecker.checkString(self.sn, min_len=0, max_len=20, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid surname'))

    try:
      ParamChecker.checkString(self.givenName, min_len=0, max_len=20, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid given name'))

    try:
      ParamChecker.checkString(self.homePostalAddress, min_len=0, max_len=255, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid address'))

    '''optional'''
    try:
      ParamChecker.checkBool(self.isMinor, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid selection for "is minor"'))

    '''optional'''
    try:
      ParamChecker.checkPhone(self.homePhone, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(ipf.message)

    '''optional'''
    try:
      ParamChecker.checkPhone(self.mobile, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid mobile number'))

    try:
      ParamChecker.checkEmail(self.mail, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(ipf.message)

    try:
      ParamChecker.checkString(self.loginShell, min_len=0, max_len=20, regex=regex.loginShell, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid login shell'))

    try:
      ParamChecker.checkDate(self.arrivalDate, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid "member since" date'))

    '''optional'''
    try:
      ParamChecker.checkDate(self.leavingDate, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid "membership canceled" date'))

    '''optional'''
    try:
      ParamChecker.checkString(self.sshPublicKey, min_len=0, max_len=1200, regex=regex.sshKey, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid SSH key'))

    '''optional'''
    try:
      ParamChecker.checkPGP(self.pgpKey, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(ipf.message)

    '''optional'''
    try:
      ParamChecker.checkiButtonUID(self.iButtonUID, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(ipf.message)

    try:
      ParamChecker.checkUsername(self.conventionSigner, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid convention signer'))

    '''optional'''
    try:
      ParamChecker.checkEmail(self.xmppID, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid XMPP/Jabber/GTalk ID'))

    '''optional'''
    try:
      ParamChecker.checkBool(self.spaceKey, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid Space-Key value'))

    '''optional'''
    try:
      ParamChecker.checkBool(self.npoMember, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid NPO-Member value'))

    try:
      ParamChecker.checkCountryCode(self.nationality, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid nationality'))

    if checkOK:
      return checkOK

    raise InvalidParameterFormat(errors)
  ####################

  def getGravatar(self, size=20):
    mail = ''

    if self.mail:
      mail = self.mail

    hashmail = hashlib.md5(mail.lower()).hexdigest()
    url = "http://www.gravatar.com/avatar/" + hashmail + "?"
    url += urllib.urlencode({'s':str(size)})

    return url

  @property
  def avatar(self):
    try:
      return base64.b64decode(self.jpegPhoto)
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      return None


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
