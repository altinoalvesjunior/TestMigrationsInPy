import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrevrange(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(
            redis.ResponseError, self.client.zrevrange,
            'a', 0, 1)
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zrevrange('a', 0, 1), [b('a3'), b('a2')])
        self.assertEquals(self.client.zrevrange('a', 1, 2), [b('a2'), b('a1')])
        self.assertEquals(
            self.client.zrevrange('a', 0, 1, withscores=True),
            [(b('a3'), 3.0), (b('a2'), 2.0)])
        self.assertEquals(
            self.client.zrevrange('a', 1, 2, withscores=True),
            [(b('a2'), 2.0), (b('a1'), 1.0)])
        # a non existant key should return empty list
        self.assertEquals(self.client.zrange('b', 0, 1, withscores=True), [])