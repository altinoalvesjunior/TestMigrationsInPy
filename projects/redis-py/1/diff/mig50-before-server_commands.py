import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_brpop(self):
        self.make_list('a', 'ab')
        self.make_list('b', 'cd')
        self.assertEquals(
            self.client.brpop(['b', 'a'], timeout=1),
            (b('b'), b('d')))
        self.assertEquals(
            self.client.brpop(['b', 'a'], timeout=1),
            (b('b'), b('c')))
        self.assertEquals(
            self.client.brpop(['b', 'a'], timeout=1),
            (b('a'), b('b')))
        self.assertEquals(
            self.client.brpop(['b', 'a'], timeout=1),
            (b('a'), b('a')))
        self.assertEquals(self.client.brpop(['b', 'a'], timeout=1), None)
        self.make_list('c', 'a')
        self.assertEquals(self.client.brpop('c', timeout=1), (b('c'), b('a')))