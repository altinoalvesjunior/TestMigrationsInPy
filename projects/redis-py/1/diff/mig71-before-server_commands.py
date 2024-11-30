import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_zrem_multiple_keys(self):
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(self.client.zrem('a', 'a1', 'a2'), 2)
        self.assertEquals(self.client.zrange('a', 0, 5), [b('a3')])