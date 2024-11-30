import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client, make_zset - igual ao mig89-before) ...

    def test_zrange(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zrange, 'a', 0, 1)
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zrange('a', 0, 1), [b('a1'), b('a2')])
        self.assertEquals(self.client.zrange('a', 1, 2), [b('a2'), b('a3')])
        self.assertEquals(
            self.client.zrange('a', 0, 1, withscores=True),
            [(b('a1'), 1.0), (b('a2'), 2.0)])
        self.assertEquals(
            self.client.zrange('a', 1, 2, withscores=True),
            [(b('a2'), 2.0), (b('a3'), 3.0)])
        # test a custom score casting function returns the correct value
        self.assertEquals(
            self.client.zrange('a', 0, 1, withscores=True,
                               score_cast_func=int),
            [(b('a1'), 1), (b('a2'), 2)])
        # a non existant key should return empty list
        self.assertEquals(self.client.zrange('b', 0, 1, withscores=True), [])