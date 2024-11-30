import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_strict_lrem(self):
        client = self.get_client(redis.StrictRedis)
        client.rpush('a', 'a1')
        client.rpush('a', 'a2')
        client.rpush('a', 'a3')
        client.rpush('a', 'a1')
        client.lrem('a', 0, 'a1')
        self.assertEquals(client.lrange('a', 0, -1), [b('a2'), b('a3')])