import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sdiffstore(self):
        # some key is not a set
        self.make_set('a', ['a1', 'a2', 'a3'])
        self.client['b'] = 'b'
        self.assertRaises(
            redis.ResponseError, self.client.sdiffstore,
            'c', ['a', 'b'])
        del self.client['b']
        self.make_set('b', ['b1', 'a2', 'b3'])
        # dest key always gets overwritten, even if it's not a set, so don't
        # test for that
        # real logic
        self.assertEquals(self.client.sdiffstore('c', ['a', 'b']), 2)
        self.assertEquals(self.client.smembers('c'), set([b('a1'), b('a3')]))