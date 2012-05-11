"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, redirect
from pylons.templating import render_mako as render
from pylons import session, request, url, config
import logging

from mematool.model.meta import Session
from mematool.lib.helpers import *
import re


class BaseController(WSGIController):
  def __init__(self):
    self.identity = None
    self.log = logging.getLogger(__name__)

    # seems to be necessary, else the connection is kept around giving unwanted results
    if 'ldapcon' in config['mematool']:
      del(config['mematool']['ldapcon'])

    # get the list of admins from the configuration file
    # replace whitespace and split on comma
    self.admins = re.sub(r' ', '', config.get('mematool.admins')).split(',')
    self.superadmins = re.sub(r' ', '', config.get('mematool.superadmins')).split(',')
    self.financeadmins = re.sub(r' ', '', config.get('mematool.financeadmins')).split(',')

  def __call__(self, environ, start_response):
    """Invoke the Controller"""
    # WSGIController.__call__ dispatches to the Controller method
    # the request is routed to. This routing information is
    # available in environ['pylons.routes_dict']
    try:
      return WSGIController.__call__(self, environ, start_response)
    finally:
      Session.remove()

  def __before__(self):
    self.identity = session.get("identity")

    if self.identity:
      request.environ["REMOTE_USER"] = self.identity

      # blind call ... we don't care about the return value
      # but only that the call sets a session variable
      # @TODO silly hack... rework
      self.isFinanceAdmin()
      self.isAdmin()
    else:
      if self._require_auth():
        referer = request.environ.get('PATH_INFO')
        session["after_login"] = referer
        self.log.debug("setting session['after_login'] to %r", referer)
        session.save()
        redirect(url(controller='auth', action='login'))

  def _require_auth(self):
    return True


  def _isParamSet(self, param):
    if param in request.params and request.params[param] != '':
      return True

    return False

  def _isParamStr(self, param, min_len=0, max_len=255, regex=None):
    if self._isParamSet(param) and len(request.params[param]) > min_len  and len(request.params[param]) <= max_len:
      if regex != None:
        if re.match(regex, request.params[param], re.IGNORECASE):
          return True
      else:
        return True

    return False

  def _isParamInt(self, param, min_val=0, min_len=0, max_len=4):
    if self._isParamStr(param, min_len, max_len) and IsInt(request.params[param]) and int(request.params[param]) >= min_val:
      return True

    return False

  def _isParamFloat(self, param, min_val=0, min_len=0, max_len=4):
    if self._isParamStr(param, min_len, max_len) and IsFloat(request.params[param]) and float(request.params[param]) >= min_val:
      return True

    return False

  def _forbidden(self):
    redirect(url(controller='error', action='forbidden'))

  @staticmethod
  def needSuperAdmin(f):
    def new_f(self):
      if self.isSuperAdmin():
        return f(self)

      self._forbidden()

    return new_f

  @staticmethod
  def needAdmin(f):
    def new_f(self):
      if self.isAdmin():
        return f(self)

      self._forbidden()

    return new_f

  @staticmethod
  def needGroup(group):
    def wrap_f(f):
      def new_f(self, *args):
        if self.isInGroup(group):
          return f(self, *args)

        self._forbidden()

      return new_f
    return wrap_f

  def isInGroup(self, group):
    if not 'identity' in session or str(group) == '' :
      return False

    session_string = 'isInGroup' + str(group)

    if not session_string in session or 1==1:
      session[session_string] = False

      if 'groups' in session:
        if hasattr(self, group):
          for ag in getattr(self, group):
            if ag in session['groups']:
              session[session_string] = True
              break

      session.save()

    return session[session_string]

  def isAdmin(self):
    if not 'identity' in session:
      return False

    if not 'isAdmin' in session:
      session['isAdmin'] = False
      if 'groups' in session:
        for ag in self.admins:
          if ag in session['groups']:
            session['isAdmin'] = True
            break

      session.save()

    return session['isAdmin']

  def isFinanceAdmin(self):
    if not 'identity' in session:
      return False

    if not 'isFinanceAdmin' in session:
      if session['identity'] in self.financeadmins:
        session['isFinanceAdmin'] = True
      else:
        session['isFinanceAdmin'] = False
        
      session.save()

    return session['isFinanceAdmin']

  @staticmethod
  def needFinanceAdmin(f):
    def new_f(self):
      if session['identity'] in self.financeadmins:
        return f(self)

      self._forbidden()

    return new_f

  '''
  @param m Member object
  @param p parameter string
  '''
  def prepareVolatileParameter(self, m, p):
    '''check if a parameter has been removed or changed'''
    if p in request.params:
      if request.params[p] == '' and p in vars(m):
        setattr(m, p, 'removed')
      else:
        setattr(m, p, request.params[p])
    elif p in vars(m) and request.params['mode'] == 'edit':
      setattr(m, p, 'removed')
