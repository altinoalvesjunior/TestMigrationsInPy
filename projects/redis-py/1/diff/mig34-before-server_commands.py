import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_getset(self):
        self.assertEquals(self.client.getset('a', 'foo'), None)
        self.assertEquals(self.client.getset('a', 'bar'), b('foo'))