import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_setnx(self):
        self.assert_(self.client.setnx('a', '1'))
        self.assertEquals(self.client['a'], b('1'))
        self.assert_(not self.client.setnx('a', '2'))
        self.assertEquals(self.client['a'], b('1'))