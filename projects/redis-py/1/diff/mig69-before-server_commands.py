import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrank(self):
        # key is not a zset
        self.client['a'] = 'a'
        self.assertRaises(redis.ResponseError, self.client.zrank, 'a', 'a4')
        del self.client['a']
        # real logic
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3, 'a4': 4, 'a5': 5})
        self.assertEquals(self.client.zrank('a', 'a1'), 0)
        self.assertEquals(self.client.zrank('a', 'a2'), 1)
        self.assertEquals(self.client.zrank('a', 'a3'), 2)
        self.assertEquals(self.client.zrank('a', 'a4'), 3)
        self.assertEquals(self.client.zrank('a', 'a5'), 4)
        # non-existent value in zset
        self.assertEquals(self.client.zrank('a', 'a6'), None)