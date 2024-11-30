import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_limited(self):
        self.make_list('a', '3214')
        self.assertEquals(
            self.client.sort('a', start=1, num=2),
            [b('2'), b('3')])