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

''' This file includes a bunch of commonly used regular expressions '''


username = r'^[a-z0-9_]{1,20}$'
email = r'\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}\b'
domain = r'^(?:[A-Z0-9-]+\.)+[A-Z]{2,4}$'
date = r'^(19\d\d|2\d\d\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'
phone = r'^\+(\d){1,3}\.(\d){4,}$'  # +123.1234   after the dot, minimum 4 numbers
homeDirectory = r'^/home/[a-z0-9_]*$'
loginShell = r'^/bin/[a-z0-9]*$'
sshKey = r'^ssh-(?:rsa AAAAB3NzaC1yc2EAAAA|dss AAAAB3NzaC1kc3MAAA)[A-Za-z0-9+/]{150,1200}'
pgpKey = r'^([a-zA-Z0-9]{4}\s*){10}$'
iButtonUID = r'^[0-9a-f]{10}$'
