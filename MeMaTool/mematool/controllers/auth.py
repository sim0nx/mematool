import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.i18n.translation import _

from mematool.lib.base import BaseController, render
from pylons.decorators.secure import https
from mematool.lib.syn2cat.auth.auth_ldap import LDAPAuthAdapter
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.lib.syn2cat.crypto import encodeAES, decodeAES


log = logging.getLogger(__name__)

class AuthController(BaseController):
  def __init__(self):
    super(AuthController, self).__init__()

  def index(self,environ):
    if self.identity is not None:
      redirect(url(controller='members', action='showAllMembers'))
    else:
      redirect(url(controller='auth', action='login'))

  @https()
  def login(self):
    if self.identity is not None:
      if 'came_from' in request.params:
        #redirect(request.params['came_from'])
        redirect(url(controller='members', action='showAllMembers'))
      else:
        redirect(url(controller='members', action='showAllMembers'))

    c.heading = 'MeMaTool'

    return render('/auth/login.mako')


  def doLogin(self):
    if not 'username' in request.params or request.params['username'] == '' or not 'password' in request.params or request.params['password'] == '':
      print "crap"
    else:
      authAdapter = LDAPAuthAdapter()
      ret = authAdapter.authenticate(request.params['username'], request.params['password'])

      if ret:
        self._clearSession()

        session['identity'] = request.params['username']
        session['secret'] = encodeAES( request.params['password'] )
        lmf = LdapModelFactory()
        session['groups'] = lmf.getUserGroupList(request.params['username'])
        # dummy call to set the variable
        self.isFinanceAdmin()
        session.save()

        log.info(request.params['username'] + ' logged in')

        if 'after_login' in session and not 'forbidden' in session["after_login"]:
          print session["after_login"]
          redirect(session["after_login"])
        else:
          if self.isAdmin():
            redirect(url(controller='members', action='index'))
          else:
            redirect(url(controller='profile', action='index'))
      else:
        session['flash'] = _('Login failed!')
        session['flash_class'] = 'error'
        session.save()

    redirect(url(controller='auth', action='login'))

  def _clearSession(self, force=False):
    if self.identity is not None or force:
      session.invalidate()
      session.delete()

  def logout(self):
    self._clearSession(force=True)
    redirect(url(controller='auth', action='login'))

  def _require_auth(self):
    return False
