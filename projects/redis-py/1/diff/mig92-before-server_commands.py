import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_get_multi(self):
        self.client['user:1'] = 'u1'
        self.client['user:2'] = 'u2'
        self.client['user:3'] = 'u3'
        self.make_list('a', '231')
        self.assertEquals(
            self.client.sort('a', get=('user:*', '#')),
            [b('u1'), b('1'), b('u2'), b('2'), b('u3'), b('3')])