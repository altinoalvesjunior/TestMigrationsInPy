import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_sort_alpha(self):
        self.make_list('a', 'ecbda')
        self.assertEquals(
            self.client.sort('a', alpha=True),
            [b('a'), b('b'), b('c'), b('d'), b('e')])