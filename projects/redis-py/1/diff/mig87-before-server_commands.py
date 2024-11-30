import unittest
import redis
from redis._compat import iteritems

class ServerCommandsTestCase(unittest.TestCase):
    def test_hmget_no_keys(self):
        self.assertRaises(redis.ResponseError, self.client.hmget, 'foo', [])