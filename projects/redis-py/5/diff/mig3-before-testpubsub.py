import unittest
from redis._compat import b, next
from redis.exceptions import ConnectionError
import redis

class PubSubRedisDownTestCase(unittest.TestCase):
    def setUp(self):
        self.connection_pool = redis.ConnectionPool(port=6390)
        self.client = redis.Redis(connection_pool=self.connection_pool)
        self.pubsub = self.client.pubsub()
    def tearDown(self):
        self.connection_pool.disconnect()
    def test_channel_subscribe(self):
        got_exception = False
        try:
            self.pubsub.subscribe('foo')
        except ConnectionError:
            got_exception = True
        self.assertTrue(got_exception)