import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_mget(self):
        self.assertEquals(self.client.mget(['a', 'b']), [None, None])
        self.client['a'] = '1'
        self.client['b'] = '2'
        self.client['c'] = '3'
        self.assertEquals(
            self.client.mget(['a', 'other', 'b', 'c']),
            [b('1'), None, b('2'), b('3')])