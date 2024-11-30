import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_setex(self):
        self.assertEquals(self.client.setex('a', '1', 60), True)
        self.assertEquals(self.client['a'], b('1'))
        self.assertEquals(self.client.ttl('a'), 60)