import unittest
import redis
from redis._compat import iteritems

class ServerCommandsTestCase(unittest.TestCase):
    def test_hmget_empty(self):
        self.assertEqual(self.client.hmget('foo', ['a', 'b']), [None, None])