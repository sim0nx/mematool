#!/usr/bin/env python

import os
from ConfigParser import ConfigParser
import unittest
import cherrypy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import mematool
from mematool import Config
from test.mematool.model.ldapModelFactory import TestLdapModelFactory


def bootstrap():
  basePath = os.path.dirname(os.path.abspath(__file__))

  config_file = basePath + '/config/mematool.conf'
  config = ConfigParser()
  if not os.path.isfile(config_file):
    raise ConfigException('Could not find config file ' +
                          config_file + ' in ' + getcwd())

  config.read(config_file)
  Config.basePath = basePath
  Config(config)

  Config.instance.db = setup_db()

def get_connection_string():
  protocol = Config.get('db', 'protocol')
  debug = Config.get_boolean('db', 'debug', False)

  if protocol == 'sqlite':
    connetionString = '{prot}:///{basepath}/{db}'.format(prot=protocol,
                                                db=Config.get('db', 'db'),
                                                basepath=Config.basePath)
  else:
    hostname = Config.get('db', 'host')
    port = Config.get('db', 'port')

    connetionString = '{prot}://{user}:{password}@{host}:{port}/{db}'.format(
      prot=protocol,
      user=Config.get('db', 'username'),
      password=Config.get('db', 'password'),
      host=hostname,
      db=Config.get('db', 'db'),
      port=port
    )

  return connetionString

def setup_db():
  db_str = get_connection_string()

  Base = declarative_base()
  sa_engine = create_engine(db_str, echo=False)
  Base.metadata.create_all(sa_engine)

  session = scoped_session(sessionmaker(autoflush=True, autocommit=False))
  session.configure(bind=sa_engine)
  
  cherrypy.request.db = session

  return session


if __name__ == "__main__":
  bootstrap()
  
  '''
  suite1 = unittest.TestLoader().loadTestsFromTestCase(TestLdapModelFactory)
  alltests = unittest.TestSuite([suite1])

  runner = unittest.TextTestRunner()
  runner.run (alltests)
  '''
  
  unittest.main()
