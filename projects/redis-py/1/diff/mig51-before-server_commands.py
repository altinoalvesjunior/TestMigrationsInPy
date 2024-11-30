import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_brpoplpush(self):
        self.make_list('a', '12')
        self.make_list('b', '34')
        self.assertEquals(self.client.brpoplpush('a', 'b'), b('2'))
        self.assertEquals(self.client.brpoplpush('a', 'b'), b('1'))
        self.assertEquals(self.client.brpoplpush('a', 'b', timeout=1), None)
        self.assertEquals(self.client.lrange('a', 0, -1), [])
        self.assertEquals(
            self.client.lrange('b', 0, -1),
            [b('1'), b('2'), b('3'), b('4')])