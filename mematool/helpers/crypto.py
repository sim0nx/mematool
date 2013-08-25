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

from Crypto.Cipher import AES
import hashlib
import base64
from mematool import Config


# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = chr(0)

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING


def encodeAES(msg):
  key = hashlib.sha256(Config.get('mematool', 'authkey')).digest()
  cipher = AES.new(key)
  return base64.b64encode(cipher.encrypt(pad(msg)))


def decodeAES(cmsg):
  key = hashlib.sha256(Config.get('mematool', 'authkey')).digest()
  cipher = AES.new(key)
  return cipher.decrypt(base64.b64decode(cmsg)).rstrip(PADDING)
