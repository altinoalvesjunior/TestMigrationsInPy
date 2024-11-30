import unittest
import redis
from redis._compat import iteritems

class ServerCommandsTestCase(unittest.TestCase):
    def test_hmset(self):
        d = {b('a'): b('1'), b('b'): b('2'), b('c'): b('3')}
        self.assert_(self.client.hmset('foo', d))
        self.assertEqual(self.client.hgetall('foo'), d)
        self.assertRaises(redis.DataError, self.client.hmset, 'foo', {})