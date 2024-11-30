import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_keys(self):
        self.assertEquals(self.client.keys(), [])
        keys = set([b('test_a'), b('test_b'), b('testc')])
        for key in keys:
            self.client[key] = 1
        self.assertEquals(
            set(self.client.keys(pattern='test_*')),
            keys - set([b('testc')]))
        self.assertEquals(set(self.client.keys(pattern='test*')), keys)