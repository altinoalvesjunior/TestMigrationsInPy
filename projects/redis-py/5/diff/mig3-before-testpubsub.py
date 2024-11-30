import unittest
from redis._compat import b, next
from redis.exceptions import ConnectionError
import redis

class PubSubRedisDownTestCase(unittest.TestCase):
    def test_channel_subscribe(self):
        got_exception = False
        try:
            self.pubsub.subscribe('foo')
        except ConnectionError:
            got_exception = True
        self.assertTrue(got_exception)