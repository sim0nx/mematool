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


class Config(object):
  instance = None

  def __init__(self, config):
    Config.instance = self
    self.config = {}
    for s in config.sections():
      if not s in self.config:
        self.config[s] = {}

      for k, v in config.items(s):
        value = v

        if v.startswith('[') and v.endswith(']'):
          value = v.lstrip('[').rstrip(']').split(',')

        self.config[s][k] = value

  @staticmethod
  def get(section, key, default=None):
    if not section in Config.instance.config:
      raise KeyError()

    if default is None and not key in Config.instance.config[section]:
      raise KeyError()

    return Config.instance.config[section].get(key, default)

  @staticmethod
  def get_boolean(section, key, default=None):
    if not section in Config.instance.config:
      raise KeyError()

    if default is None and not key in Config.instance.config[section]:
      raise KeyError()

    if not Config.instance.config[section].get(key, default).lower() in ['true', 'false']:
      raise ValueError()

    if Config.instance.config[section].get(key, default).lower() == 'true':
      return True

    return False
