import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client, make_zset - igual ao mig89-before) ...
    def test_zinterstore(self):
        self.make_zset('a', {'a1': 1, 'a2': 1, 'a3': 1})
        self.make_zset('b', {'a1': 2, 'a3': 2, 'a4': 2})
        self.make_zset('c', {'a1': 6, 'a3': 5, 'a4': 4})
        # sum, no weight
        self.assert_(self.client.zinterstore('z', ['a', 'b', 'c']))
        self.assertEquals(
            self.client.zrange('z', 0, -1, withscores=True),
            [(b('a3'), 8), (b('a1'), 9)]
        )
        # max, no weight
        self.assert_(
            self.client.zinterstore('z', ['a', 'b', 'c'], aggregate='MAX')
        )
        self.assertEquals(
            self.client.zrange('z', 0, -1, withscores=True),
            [(b('a3'), 5), (b('a1'), 6)]
        )
        # with weight
        self.assert_(self.client.zinterstore('z', {'a': 1, 'b': 2, 'c': 3}))
        self.assertEquals(
            self.client.zrange('z', 0, -1, withscores=True),
            [(b('a3'), 20), (b('a1'), 23)]
        )