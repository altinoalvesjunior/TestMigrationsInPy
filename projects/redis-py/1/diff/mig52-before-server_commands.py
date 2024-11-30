import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_brpoplpush_empty_string(self):
        self.client.lpush('a', '')
        self.assertEquals(self.client.brpoplpush('a', 'b'), b(''))