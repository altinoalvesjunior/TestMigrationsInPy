import unittest
import redis
from redis._compat import iteritems

class ServerCommandsTestCase(unittest.TestCase):
    def test_hmget(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assert_(self.client.hmset('foo', d))
        self.assertEqual(
            self.client.hmget('foo', ['a', 'b', 'c']), [b('1'), b('2'), b('3')]
        )
        self.assertEqual(
            self.client.hmget('foo', ['a', 'c']), [b('1'), b('3')]
        )
        # using *args type args
        self.assertEquals(self.client.hmget('foo', 'a', 'c'), [b('1'), b('3')])