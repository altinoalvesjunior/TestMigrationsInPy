import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zscore(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zscore, 'a', 'a1')
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 0, 'a2': 1, 'a3': 2})
        self.assertEquals(self.client.zscore('a', 'a1'), 0.0)
        self.assertEquals(self.client.zscore('a', 'a2'), 1.0)
        # test a non-existant member
        self.assertEquals(self.client.zscore('a', 'a4'), None)