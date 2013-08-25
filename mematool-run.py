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

import cherrypy
import os
from ConfigParser import ConfigParser
from mematool.helpers.i18ntool import ugettext as _
from mematool.helpers.i18ntool import I18nTool
from mematool import Config
from mematool.model.satool import SAEnginePlugin, SATool
from mematool.controllers.index import IndexController
from mematool.controllers.profile import ProfileController
from mematool.controllers.members import MembersController
from mematool.controllers.payments import PaymentsController
from mematool.controllers.mails import MailsController
from mematool.controllers.groups import GroupsController
from mematool.controllers.statistics import StatisticsController
from mematool.controllers.preferences import PreferencesController
from cherrypy._cperror import HTTPRedirect


def application(environ, start_response):
  bootstap()
  return cherrypy.tree(environ, start_response)


def require_auth():
  if not 'user' in cherrypy.session:
    raise HTTPRedirect('/doLogin')


def bootstap():
  basePath = os.path.dirname(os.path.abspath(__file__))

  config_file = basePath + '/config/mematool.conf'
  config = ConfigParser()
  if not os.path.isfile(config_file):
    raise ConfigException('Could not find config file ' +
                          config_file + ' in ' + getcwd())

  config.read(config_file)
  Config.basePath = basePath
  Config(config)

  wsgi_config = basePath + '/config/cherrypy.conf'
  cherrypy.config.update(config=wsgi_config)

  cherrypy_config = {'tools.staticdir.on': True,
                     'tools.staticdir.root': basePath + "/htdocs",
                     'tools.staticdir.dir': "",
                     'tools.sessions.on': True,
                     'tools.sessions.storage_type': 'file',
                     'tools.sessions.storage_path': basePath + '/sessions',
                     'tools.sessions.timeout': 60,
                     }

  cherrypy.config.update(cherrypy_config)

  cherrypy.tools.I18nTool = I18nTool(basePath)
  cherrypy.tools.require_auth = cherrypy.Tool('before_handler', require_auth)
  # DB stuff
  SAEnginePlugin(cherrypy.engine).subscribe()
  cherrypy.tools.db = SATool()

  cherrypy.tree.mount(IndexController(), '/')
  cherrypy.tree.mount(ProfileController(), '/profile')
  cherrypy.tree.mount(MembersController(), '/members')
  cherrypy.tree.mount(PaymentsController(), '/payments')
  cherrypy.tree.mount(MailsController(), '/mails')
  cherrypy.tree.mount(GroupsController(), '/groups')
  cherrypy.tree.mount(StatisticsController(), '/statistics')
  cherrypy.tree.mount(PreferencesController(), '/preferences')


if __name__ == '__main__':
  bootstap()
  try:
      # this is the way it should be done in cherrypy 3.X
      cherrypy.engine.start()
      cherrypy.engine.block()
  except Exception as e:
    print e
