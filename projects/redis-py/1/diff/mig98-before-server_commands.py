import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_desc(self):
        self.make_list('a', '231')
        self.assertEquals(
            self.client.sort('a', desc=True),
            [b('3'), b('2'), b('1')])