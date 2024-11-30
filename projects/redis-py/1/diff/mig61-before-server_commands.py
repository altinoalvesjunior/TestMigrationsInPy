import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zcount(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zcount, 'a', 0, 0)
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zcount('a', '-inf', '+inf'), 3)
        self.assertEquals(self.client.zcount('a', 1, 2), 2)
        self.assertEquals(self.client.zcount('a', 10, 20), 0)