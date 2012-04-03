#
# MeMaTool (c) 2010 Georges Toth <georges _at_ trypill _dot_ org>
#
#
# This file is part of MeMaTool.
#
#
# MeMaTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MeMaTool.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-


from mematool.model.meta import Base

from datetime import date
from mematool.lib.base import Session
from mematool.model import TmpMember

import hashlib
from binascii import b2a_base64, a2b_base64
from mematool.lib.syn2cat import regex
from mematool.model.lechecker import ParamChecker, InvalidParameterFormat
import os

import gettext
_ = gettext.gettext


class Member():
  # ldap
  str_vars = ['uid',\
    'cn',\
    'sn',\
    'givenName',\
    'homePhone',\
    'mobile',\
    'mail',\
    'xmppID',\
    'userPassword',\
    'sambaNTPassword',\
    'sambaSID',\
    'sshPublicKey',\
    'pgpKey',\
    'iButtonUID',\
    'conventionSigner',\
    'uidNumber',\
    'gidNumber',\
    'loginShell',\
    'hDirectory',\
    'birthDate',\
    'homePostalAddress',\
    'arrivalDate',\
    'leavingDate']
  list_vars = ['groups']
  bool_vars = ['fullMember',\
    'lockedMember']

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
  birthDate = '' # birthDate
  homePostalAddress = '' # homePostalAddress
  arrivalDate = '' # member since
  leavingDate = '' # membership canceled
  groups = [] # additional user groups
  fullMember = False
  lockedMember = False
  '''
  

  def __init__(self):
    for v in self.str_vars:
      setattr(self, v, '')
    for v in self.list_vars:
      setattr(self, v, [])
    for v in self.bool_vars:
      setattr(self, v, False)

    self.all_vars = []
    self.all_vars.extend(self.str_vars)
    self.all_vars.extend(self.list_vars)
    self.all_vars.extend(self.bool_vars)

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
    self.sambaSID = serverSambaSID + '-' + str( (int(self.uidNumber) * 2) + 1000 )


  ####################
  # checker interface
  def check(self):
    errors = []
    checkOK = True

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
      ParamChecker.checkDate(self.birthDate, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid birth date'))

    try:
      ParamChecker.checkString(self.homePostalAddress, min_len=0, max_len=255, param=False)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid address'))

    '''optional'''
    try:
      ParamChecker.checkPhone(self.homePhone, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(ipf.message)

    try:
      ParamChecker.checkPhone(self.mobile, param=False)
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

    '''optional'''
    try:
      ParamChecker.checkUsername(self.conventionSigner, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid convention signer'))

    '''optional'''
    try:
      ParamChecker.checkEmail(self.xmppID, param=False, optional=True)
    except InvalidParameterFormat as ipf:
      checkOK = False
      errors.append(_('Invalid XMPP/Jabber/GTalk ID'))


    if checkOK:
      return checkOK

    raise InvalidParameterFormat(errors)
  ####################
