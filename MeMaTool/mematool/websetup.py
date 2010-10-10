"""Setup the MeMaTool application"""
import logging

import pylons.test

from mematool.config.environment import load_environment
from mematool.model.meta import Session, metadata, Base


log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup mematool here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    metadata.create_all(bind=Session.bind)



    log.info("Creating tables")
    #Base.metadata.drop_all(checkfirst=True, bind=Session.bind)
    Base.metadata.create_all(bind=Session.bind)
    log.info("Successfully setup")


    Session.commit()
