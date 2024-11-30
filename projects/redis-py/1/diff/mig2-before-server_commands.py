import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_dbsize(self):
        self.client['a'] = 'foo'
        self.client['b'] = 'bar'
        self.assertEquals(self.client.dbsize(), 2)