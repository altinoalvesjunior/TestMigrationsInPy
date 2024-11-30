import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_ping(self):
        self.assertEquals(self.client.ping(), True)