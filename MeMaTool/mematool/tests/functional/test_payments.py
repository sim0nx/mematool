from mematool.tests import *

class TestPaymentsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='payments', action='index'))
        # Test response...
