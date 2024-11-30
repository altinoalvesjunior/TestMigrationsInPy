import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrevrank(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zrevrank, 'a', 'a4')
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 5, 'a2': 4, 'a3': 3, 'a4': 2, 'a5': 1})
        self.assertEquals(self.client.zrevrank('a', 'a1'), 0)
        self.assertEquals(self.client.zrevrank('a', 'a2'), 1)
        self.assertEquals(self.client.zrevrank('a', 'a3'), 2)
        self.assertEquals(self.client.zrevrank('a', 'a4'), 3)
        self.assertEquals(self.client.zrevrank('a', 'a5'), 4)
        self.assertEquals(self.client.zrevrank('a', 'b'), None)