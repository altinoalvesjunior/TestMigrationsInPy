import unittest
import redis
from redis._compat import iteritems

class ServerCommandsTestCase(unittest.TestCase):
    def test_mset(self):
        d = {'a': '1', 'b': '2', 'c': '3'}
        self.assert_(self.client.mset(d))
        for k, v in iteritems(d):
            self.assertEquals(self.client[k], b(v))