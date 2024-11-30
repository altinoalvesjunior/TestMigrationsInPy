import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zcard(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zcard, 'a')
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zcard('a'), 3)