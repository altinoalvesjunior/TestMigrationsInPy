import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrem(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zrem, 'a', 'a1')
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zrem('a', 'a2'), 1)
        self.assertEquals(self.client.zrange('a', 0, 5), [b('a1'), b('a3')])
        self.assertEquals(self.client.zrem('a', 'b'), 0)
        self.assertEquals(self.client.zrange('a', 0, 5), [b('a1'), b('a3')])