import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrevrangebyscore(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(
            redis.ResponseError, self.client.zrevrangebyscore,
            'a', 0, 1)
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3, 'a4': 4, 'a5': 5})
        self.assertEquals(
            self.client.zrevrangebyscore('a', 4, 2),
            [b('a4'), b('a3'), b('a2')])
        self.assertEquals(
            self.client.zrevrangebyscore('a', 4, 2, start=1, num=2),
            [b('a3'), b('a2')])
        self.assertEquals(
            self.client.zrevrangebyscore('a', 4, 2, withscores=True),
            [(b('a4'), 4.0), (b('a3'), 3.0), (b('a2'), 2.0)])
        # a non existant key should return empty list
        self.assertEquals(
            self.client.zrevrangebyscore('b', 1, 0, withscores=True),
            [])