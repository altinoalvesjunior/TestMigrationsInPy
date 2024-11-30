import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_strict_zadd(self):
        client = self.get_client(redis.StrictRedis)
        client.zadd('a', 1.0, 'a1', 2.0, 'a2', a3=3.0)
        self.assertEquals(client.zrange('a', 0, 3, withscores=True),
                          [(b('a1'), 1.0), (b('a2'), 2.0), (b('a3'), 3.0)])