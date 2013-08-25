import unittest
import mematool
import mematool.model.ldapmodel
import mematool.model.dbmodel
from mematool.model.ldapModelFactory import LdapModelFactory
from mematool.helpers.ldapConnector import LdapConnector


class TestLdapModelFactory(unittest.TestCase):
  def setUp(self):
    unittest.TestCase.setUp(self)
    
    self.username = 'mematool_test'
    self.password = 'mematool_test'
    
    ldap_connector = LdapConnector(username=self.username, password=self.password)
    self.ldapcon = ldap_connector.get_connection()
    self.ldmf = LdapModelFactory(self.ldapcon)

  def tearDown(self):
    unittest.TestCase.tearDown(self)
    self.ldapcon = None

  ################# User
  def test_getUser(self):
    user = self.ldmf.getUser(self.username)
    self.assertIsInstance(user, mematool.model.ldapmodel.Member)

  def test_getUserList(self):
    o = self.ldmf.getUserList()
    self.assertIsInstance(o, list)
    self.assertGreaterEqual(len(o), 1)

  def test_getActiveMemberList(self):
    o = self.ldmf.getActiveMemberList()
    self.assertIsInstance(o, list)
    self.assertGreaterEqual(len(o), 1)

  def test_getUserGroupList(self):
    o = self.ldmf.getUserGroupList(self.username)
    self.assertIsInstance(o, list)
    self.assertGreaterEqual(len(o), 1)

  def test_getHighestUidNumber(self):
    o = self.ldmf.getHighestUidNumber()
    self.assertIsInstance(o, str)
    self.assertRegexpMatches(o, r'^\d+$')
    o = int(o)
    self.assertGreaterEqual(o, 1000)

  def test_getUidNumberFromUid(self):
    o = self.ldmf.getUidNumberFromUid(self.username)
    self.assertIsInstance(o, str)
    self.assertRegexpMatches(o, r'^\d+$')
    o = int(o)
    self.assertGreaterEqual(o, 1000)

  '''
  def test_prepareVolatileAttribute(self):
    # @todo
    raise NotImplemented()

  def test__updateMember(self):
    # @todo
    raise NotImplemented()

  def test__addMember(self):
    # @todo
    raise NotImplemented()

  def test_deleteUser(self):
    # @todo
    raise NotImplemented()

  def test_changeUserGroup(self):
    # @todo
    raise NotImplemented()

  def test_updateAvatar(self):
    # @todo
    raise NotImplemented()
  '''

  ################# Group

  def test_getGroup(self):
    user = self.ldmf.getUser(self.username)
    self.assertIsInstance(user.groups, list)
    self.assertGreaterEqual(len(user.groups), 1)
    
    for g in user.groups:
      group = self.ldmf.getGroup(g)
      self.assertIsInstance(group, mematool.model.dbmodel.Group)

  def test_getGroupList(self):
    o = self.ldmf.getGroupList()
    self.assertIsInstance(o, list)
    self.assertGreaterEqual(len(o), 1)

  def test_getGroupMembers(self):
    user = self.ldmf.getUser(self.username)
    self.assertIsInstance(user.groups, list)
    self.assertGreaterEqual(len(user.groups), 1)
    
    for g in user.groups:
      o = self.ldmf.getGroupMembers(g)
      self.assertIsInstance(o, list)
      self.assertGreaterEqual(len(o), 1)

  def test_addDeleteGroup(self):
    # add
    self.assertTrue(self.ldmf.addGroup('test_group'))
    o = self.ldmf.getGroupList()
    self.assertIn('test_group', o)

    # delete
    self.assertTrue(self.ldmf.deleteGroup('test_group'))
    o = self.ldmf.getGroupList()
    self.assertNotIn('test_group', o)

  def test_getHighestGidNumber(self):
    o = self.ldmf.getHighestGidNumber()
    self.assertIsInstance(o, str)
    self.assertRegexpMatches(o, r'^\d+$')
    o = int(o)
    self.assertGreaterEqual(o, 1000)

  ################# Domain

  def test_addDeleteDomain(self):
    res = self.ldmf.addDomain('example.com')
    self.assertTrue(res)

    res = self.ldmf.getDomainList()
    self.assertIn('example.com', res)

    res = self.ldmf.deleteDomain('example.com')
    self.assertTrue(res)

    res = self.ldmf.getDomainList()
    self.assertNotIn('example.com', res)

  def test_getDomain(self):
    res = self.ldmf.addDomain('example.com')
    self.assertTrue(res)

    d = self.ldmf.getDomain('example.com')
    self.assertIsInstance(d, mematool.model.ldapmodel.Domain)

    res = self.ldmf.deleteDomain('example.com')
    self.assertTrue(res)

  def test_getDomainList(self):
    res = self.ldmf.getDomainList()
    self.assertIsInstance(res, list)

  ################# Alias

  def test_getAlias(self):                                                                                                                                                                                                                
    res = self.ldmf.addDomain('example.com')

    alias = mematool.model.ldapmodel.Alias()
    alias.dn_mail = 'test1@example.com'
    alias.mail = ['test2@example.com']
    alias.maildrop = ['test3@example.com']

    try:
      res = self.ldmf.addAlias(alias)
      self.assertTrue(res)
    except mematool.helpers.exceptions.EntryExists:
      pass

    res = self.ldmf.getAlias('test1@example.com')
    self.assertIsInstance(res, mematool.model.ldapmodel.Alias)
    
    res = self.ldmf.deleteAlias('test1@example.com')
    self.assertTrue(res)

    res = self.ldmf.deleteDomain('example.com')
    self.assertTrue(res)

  def test_getAliasList(self):                                                                                                                                                                                                           
    res = self.ldmf.getAliasList('example.com')
    self.assertIsInstance(res, list)

  def test_getMaildropList(self):                                                                                                                                                                                                           
    res = self.ldmf.getMaildropList('test3@example.com')
    self.assertIsInstance(res, dict)

  def test_addDeleteAlias(self):
    res = self.ldmf.addDomain('example.com')
    #self.assertTrue(res)

    alias = mematool.model.ldapmodel.Alias()
    alias.dn_mail = 'test1@example.com'
    alias.mail = ['test2@example.com']
    alias.maildrop = ['test3@example.com']

    try:
      res = self.ldmf.addAlias(alias)
      self.assertTrue(res)
    except mematool.helpers.exceptions.EntryExists:
      pass
    
    res = self.ldmf.deleteAlias('test1@example.com')
    self.assertTrue(res)

    res = self.ldmf.deleteDomain('example.com')
    self.assertTrue(res)

  '''
  def test_updateAlias(self):                                                                                                                                                                                                             
    # @todo
    raise NotImplemented()

  def test_deleteMaildrop(self):                                                                                                                                                                                                     
    # @todo
    raise NotImplemented()
  '''
