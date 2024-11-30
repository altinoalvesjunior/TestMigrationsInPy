import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_floating_point_encoding(self):
        """
        High precision floating point values sent to the server should keep
        precision.
        """
        timestamp = 1349673917.939762
        self.client.zadd('a', 'aaa', timestamp)
        self.assertEquals(self.client.zscore('a', 'aaa'), timestamp)