import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_rpoplpush(self):
        # no src key
        self.make_list('b', ['b1'])
        self.assertEquals(self.client.rpoplpush('a', 'b'), None)
        # no dest key
        self.assertEquals(self.client.rpoplpush('b', 'a'), b('b1'))
        self.assertEquals(self.client.lindex('a', 0), b('b1'))
        del self.client['a']
        del self.client['b']
        # src key is not a list
        self.client['a'] = 'a1'
        self.assertRaises(redis.ResponseError, self.client.rpoplpush, 'a', 'b')
        del self.client['a']
        # dest key is not a list
        self.make_list('a', ['a1'])
        self.client['b'] = 'b'
        self.assertRaises(redis.ResponseError, self.client.rpoplpush, 'a', 'b')
        del self.client['a']
        del self.client['b']
        # real logic
        self.make_list('a', ['a1', 'a2', 'a3'])
        self.make_list('b', ['b1', 'b2', 'b3'])
        self.assertEquals(self.client.rpoplpush('a', 'b'), b('a3'))
        self.assertEquals(self.client.lrange('a', 0, 2), [b('a1'), b('a2')])
        self.assertEquals(
            self.client.lrange('b', 0, 4),
            [b('a3'), b('b1'), b('b2'), b('b3')])