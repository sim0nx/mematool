# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Georges Toth <georges _at_ trypill _dot_ org>
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

import os
import cherrypy
import urllib
import hashlib
import base64
from binascii import b2a_base64
from mematool import Config
from mematool.helpers import regex
from mematool.helpers.lechecker import ParamChecker, InvalidParameterFormat
from mematool.model.dbmodel import TmpMember
from mematool.helpers.i18ntool import ugettext as _


class BaseObject(object):
  str_vars = []
  list_vars = []
  bool_vars = []
  bin_vars = []
  no_auto_update_vars = []

  def __init__(self):
    self.auto_update_vars = []

    for v in self.str_vars:
      setattr(self, v, '')
      if not v in self.no_auto_update_vars:
        self.auto_update_vars.append(v)

    for v in self.list_vars:
      setattr(self, v, [])

    for v in self.bool_vars:
      setattr(self, v, False)
      if not v in self.no_auto_update_vars:
        self.auto_update_vars.append(v)

    for v in self.bin_vars:
      setattr(self, v, None)
      if not v in self.no_auto_update_vars:
        self.auto_update_vars.append(v)

    self.all_vars = []
    self.all_vars.extend(self.str_vars)
    self.all_vars.extend(self.list_vars)
    self.all_vars.extend(self.bool_vars)
    self.all_vars.extend(self.bin_vars)

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

  def set_property(self, key, value):
    if key in self.bool_vars:
      if value.lower() == 'true':
        setattr(self, key, True)
      else:
        setattr(self, key, False)
    elif key in self.bin_vars:
      setattr(self, key, value)
    elif not value is None and not isinstance(value, unicode):
      value_ = unicode(str(value), 'utf-8')
      setattr(self, key, value_)
    else:
      setattr(self, key, value)


class Member(BaseObject):
  # ldap
  str_vars = ['uid',
              'sn',
              'cn',
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
              'homeDirectory',
              'homePostalAddress',
              'arrivalDate',
              'leavingDate',
              'nationality']
  list_vars = ['groups']
  bool_vars = ['spaceKey',
               'npoMember',
               'isMinor']
  bin_vars = ['jpegPhoto']
  no_auto_update_vars = ['userPassword',
                         'sambaNTPassword',
                         'sambaSID',
                         'uidNumber',
                         'uid',
                         'jpegPhoto']

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
    super(Member, self).__init__()

  def __repr__(self):
    return '''<Member('uidNumber=%s, uid=%s, validate=%s')>'''.format(self.uidNumber, self.uid, self.validate)

  @property
  def validate(self):
    if not self.uidNumber == '':
      if cherrypy.request.db.query(TmpMember).filter(TmpMember.id == self.uidNumber).count() > 0:
        return True

    return False

  @property
  def cn(self):
    return u'{0} {1}'.format(self.givenName, self.sn)

  @cn.setter
  def cn(self, value):
    # this code is not used it only exists for the way
    # the code is currently implemented with auto-filling vars etc
    # @todo: rework
    pass

  @property
  def gn(self):
    return self.givenName

  @property
  def homeDirectory(self):
    return Config.get('posix', 'base_home') + '/' + self.uid

  @homeDirectory.setter
  def homeDirectory(self, value):
    # this code is not used it only exists for the way
    # the code is currently implemented with auto-filling vars etc
    # @todo: rework
    pass

  @property
  def gidNumber(self):
    # @TODO review: for now we don't allow custom GIDs
    return Config.get('posix', 'default_gid')

  @gidNumber.setter
  def gidNumber(self, value):
    # this code is not used it only exists for the way
    # the code is currently implemented with auto-filling vars etc
    # @todo: rework
    pass

  @property
  def nationality(self):
    return self._nationality

  @nationality.setter
  def nationality(self, value):
    self._nationality = value.upper()

  @property
  def fullMember(self):
    return self.is_in_group(Config.get('mematool', 'group_fullmember'))

  @property
  def lockedMember(self):
    return self.is_in_group(Config.get('mematool', 'group_lockedmember'))

  def is_in_group(self, group):
    if group in self.groups:
      return True

    return False

  def is_admin(self):
    for g in Config.get('mematool', 'admin_group'):
      if self.is_in_group(g):
        return True

    for u in Config.get('mematool', 'admin_user'):
      if self.uid == u:
        return True

    return False

  def is_finance_admin(self):
    for u in Config.get('mematool', 'admin_finance'):
      if self.uid == u:
        return True

    return False

  def setPassword(self, password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    self.userPassword = '{SSHA}' + b2a_base64(h.digest() + salt)[:-1]
    self.sambaNTPassword = hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()

  def generateUserSID(self):
    #@TODO put in config file
    serverSambaSID = 'S-1-1-1'
    self.sambaSID = '{0}-{1}'.format(serverSambaSID, ((int(self.uidNumber) * 2) + 1000))

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
    if self.mail:
      mail = self.mail
    else:
      mail = ''

    hashmail = hashlib.md5(mail.lower()).hexdigest()
    url = 'http://www.gravatar.com/avatar/{0}?'.format(hashmail)
    url += urllib.urlencode({'s': str(size)})

    return url

  @property
  def avatar(self):
    try:
      return base64.b64decode(self.jpegPhoto)
    except:
      import sys, traceback
      traceback.print_exc(file=sys.stdout)
      return None


class Domain(BaseObject):
  str_vars = ['dc']

  def __repr__(self):
    return "<Domain('dc=%s')>" % (self.dc)


class Alias(BaseObject):
  str_vars = ['dn_mail']
  list_vars = ['mail', 'maildrop']

  def __repr__(self):
    return "<Alias('dn_mail=%s')>" % (self.dn_mail)

  @property
  def domain(self):
    if not self.dn_mail == '':
      return self.dn_mail.split('@')[1]

    return None

  def getDN(self, basedn):
    if not self.dn_mail == '':
      return 'mail=' + self.dn_mail + ',dc=' + self.domain + ',' + basedn

    raise Exception('Uninitialized object')
