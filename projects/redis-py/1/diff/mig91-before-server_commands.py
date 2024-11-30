import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_get(self):
        self.client['user:1'] = 'u1'
        self.client['user:2'] = 'u2'
        self.client['user:3'] = 'u3'
        self.make_list('a', '231')
        self.assertEquals(
            self.client.sort('a', get='user:*'),
            [b('u1'), b('u2'), b('u3')])