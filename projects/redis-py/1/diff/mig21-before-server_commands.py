import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_getrange(self):
        self.client['a'] = 'foo'
        self.assertEquals(self.client.getrange('a', 0, 0), b('f'))
        self.assertEquals(self.client.getrange('a', 0, 2), b('foo'))
        self.assertEquals(self.client.getrange('a', 3, 4), b(''))