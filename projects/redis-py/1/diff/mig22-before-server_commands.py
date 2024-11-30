import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_decr(self):
        self.assertEquals(self.client.decr('a'), -1)
        self.assertEquals(self.client['a'], b('-1'))
        self.assertEquals(self.client.decr('a'), -2)
        self.assertEquals(self.client['a'], b('-2'))
        self.assertEquals(self.client.decr('a', amount=5), -7)
        self.assertEquals(self.client['a'], b('-7'))