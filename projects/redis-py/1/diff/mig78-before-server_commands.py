import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client, make_zset - igual ao mig89-before) ...

    def test_zunionstore(self):
        self.make_zset('a', {'a1': 1, 'a2': 1, 'a3': 1})
        self.make_zset('b', {'a1': 2, 'a3': 2, 'a4': 2})
        self.make_zset('c', {'a1': 6, 'a4': 5, 'a5': 4})
        # sum, no weight
        self.assert_(self.client.zunionstore('z', ['a', 'b', 'c']))
        self.assertEquals(
            self.client.zrange('z', 0, -1, withscores=True),
            [
                (b('a2'), 1),
                (b('a3'), 3),
                (b('a5'), 4),
                (b('a4'), 7),
                (b('a1'), 9)
            ]
        )
        # max, no weight
        self.assert_(
            self.client.zunionstore('z', ['a', 'b', 'c'], aggregate='MAX')
        )
        self.assertEquals(
            self.client.zrange('z', 0, -1, withscores=True),
            [
                (b('a2'), 1),
                (b('a3'), 2),
                (b('a5'), 4),
                (b('a4'), 5),
                (b('a1'), 6)
            ]
        )
        # with weight
        self.assert_(self.client.zunionstore('z', {'a': 1, 'b': 2, 'c': 3}))
        self.assertEquals(
            self.client.zrange('z', 0, -1, withscores=True),
            [
                (b('a2'), 1),
                (b('a3'), 5),
                (b('a5'), 12),
                (b('a4'), 19),
                (b('a1'), 23)
            ]
        )