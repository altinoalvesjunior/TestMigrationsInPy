import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_basic(self):
        self.make_list('a', '3214')
        self.assertEquals(
            self.client.sort('a'),
            [b('1'), b('2'), b('3'), b('4')])