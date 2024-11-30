import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_debug_object(self):
        self.client['a'] = 'foo'
        debug_info = self.client.debug_object('a')
        self.assert_(len(debug_info) > 0)
        self.assertEquals(debug_info['refcount'], 1)
        self.assert_(debug_info['serializedlength'] > 0)
        self.client.rpush('b', 'a1')
        debug_info = self.client.debug_object('a')