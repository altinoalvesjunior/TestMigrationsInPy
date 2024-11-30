import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_randomkey(self):
        self.assertEquals(self.client.randomkey(), None)
        self.client['a'] = '1'
        self.client['b'] = '2'
        self.client['c'] = '3'
        self.assert_(self.client.randomkey() in (b('a'), b('b'), b('c')))