import unittest
import redis
from redis._compat import iteritems, b

class ServerCommandsTestCase(unittest.TestCase):
    def test_binary_lists(self):
        mapping = {
            b('foo bar'): [b('1'), b('2'), b('3')],
            b('foo\r\nbar\r\n'): [b('4'), b('5'), b('6')],
            b('foo\tbar\x07'): [b('7'), b('8'), b('9')],
        }
        # fill in lists
        for key, value in iteritems(mapping):
            for c in value:
                self.assertTrue(self.client.rpush(key, c))
        # check that KEYS returns all the keys as they are
        self.assertEqual(sorted(self.client.keys('*')),
                         sorted(list(iteritems(mapping)))) #No original usa iteritems, não iterkeys
        # check that it is possible to get list content by key name
        for key in iteritems(mapping): #No original usa iteritems, não iterkeys
            self.assertEqual(self.client.lrange(key, 0, -1),
                             mapping[key])