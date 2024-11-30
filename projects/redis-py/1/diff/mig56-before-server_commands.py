import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_rpushx(self):
        # key is not a list
        self.client['a'] = 'b'
        self.assertRaises(redis.ResponseError, self.client.rpushx, 'a', 'a')
        del self.client['a']
        # real logic
        self.assertEquals(self.client.rpushx('a', 'b'), 0)
        self.assertEquals(self.client.lrange('a', 0, -1), [])
        self.make_list('a', 'abc')
        self.assertEquals(self.client.rpushx('a', 'd'), 4)
        self.assertEquals(
            self.client.lrange('a', 0, -1),
            [b('a'), b('b'), b('c'), b('d')])