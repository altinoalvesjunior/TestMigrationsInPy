import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_response_callbacks(self):
        self.assertEquals(
            self.client.response_callbacks,
            redis.Redis.RESPONSE_CALLBACKS)
        self.assertNotEquals(
            id(self.client.response_callbacks),
            id(redis.Redis.RESPONSE_CALLBACKS))
        self.client.set_response_callback('GET', lambda x: 'static')
        self.client.set('a', 'foo')
        self.assertEquals(self.client.get('a'), 'static')