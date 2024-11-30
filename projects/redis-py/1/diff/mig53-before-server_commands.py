import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_lset(self):
        # no key
        self.assertRaises(redis.ResponseError, self.client.lset, 'a', 1, 'b')
        # key is not a list
        self.client['a'] = 'b'
        self.assertRaises(redis.ResponseError, self.client.lset, 'a', 1, 'b')
        del self.client['a']
        # real logic
        self.make_list('a', 'abc')
        self.assertEquals(
            self.client.lrange('a', 0, 2),
            [b('a'), b('b'), b('c')])
        self.assert_(self.client.lset('a', 1, 'd'))
        self.assertEquals(
            self.client.lrange('a', 0, 2),
            [b('a'), b('d'), b('c')])