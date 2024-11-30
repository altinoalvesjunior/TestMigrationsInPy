import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_append(self):
        # invalid key type
        self.client.rpush('a', 'a1')
        self.assertRaises(redis.ResponseError, self.client.append, 'a', 'a1')
        del self.client['a']
        # real logic
        self.assertEquals(self.client.append('a', 'a1'), 2)
        self.assertEquals(self.client['a'], b('a1'))
        self.assert_(self.client.append('a', 'a2'), 4)
        self.assertEquals(self.client['a'], b('a1a2'))