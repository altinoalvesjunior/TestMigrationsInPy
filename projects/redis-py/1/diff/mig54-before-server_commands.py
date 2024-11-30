import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_rpop(self):
        # no key
        self.assertEquals(self.client.rpop('a'), None)
        # key is not a list
        self.client['a'] = 'b'
        self.assertRaises(redis.ResponseError, self.client.rpop, 'a')
        del self.client['a']
        # real logic
        self.make_list('a', 'abc')
        self.assertEquals(self.client.rpop('a'), b('c'))
        self.assertEquals(self.client.rpop('a'), b('b'))
        self.assertEquals(self.client.rpop('a'), b('a'))
        self.assertEquals(self.client.rpop('a'), None)