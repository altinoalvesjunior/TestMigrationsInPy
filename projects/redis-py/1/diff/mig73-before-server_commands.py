import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zremrangebyscore(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(
            redis.ResponseError, self.client.zremrangebyscore,
            'a', 0, 1)
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3, 'a4': 4, 'a5': 5})
        self.assertEquals(self.client.zremrangebyscore('a', 2, 4), 3)
        self.assertEquals(self.client.zrange('a', 0, 5), [b('a1'), b('a5')])
        self.assertEquals(self.client.zremrangebyscore('a', 2, 4), 0)
        self.assertEquals(self.client.zrange('a', 0, 5), [b('a1'), b('a5')])