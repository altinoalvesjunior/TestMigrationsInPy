import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def make_zset(self, name, d):
        for k, v in d.items():
            self.client.zadd(name, **{k: v})

    def test_zadd(self):
        self.make_zset('a', {'a1': 1, 'a2': 2, 'a3': 3})
        self.assertEquals(
            self.client.zrange('a', 0, 3),
            [b('a1'), b('a2'), b('a3')])