import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrangebyscore(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(
            redis.ResponseError, self.client.zrangebyscore,
            'a', 0, 1)
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3, 'a4': 4, 'a5': 5})
        self.assertEquals(
            self.client.zrangebyscore('a', 2, 4),
            [b('a2'), b('a3'), b('a4')])
        self.assertEquals(
            self.client.zrangebyscore('a', 2, 4, start=1, num=2),
            [b('a3'), b('a4')])
        self.assertEquals(
            self.client.zrangebyscore('a', 2, 4, withscores=True),
            [(b('a2'), 2.0), (b('a3'), 3.0), (b('a4'), 4.0)])
        # a non existant key should return empty list
        self.assertEquals(
            self.client.zrangebyscore('b', 0, 1, withscores=True), [])