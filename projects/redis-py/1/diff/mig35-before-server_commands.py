import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_incr(self):
        self.assertEquals(self.client.incr('a'), 1)
        self.assertEquals(self.client['a'], b('1'))
        self.assertEquals(self.client.incr('a'), 2)
        self.assertEquals(self.client['a'], b('2'))
        self.assertEquals(self.client.incr('a', amount=5), 7)
        self.assertEquals(self.client['a'], b('7'))