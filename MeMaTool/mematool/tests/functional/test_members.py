from mematool.tests import *

class TestMembersController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='members', action='index'))
        # Test response...
