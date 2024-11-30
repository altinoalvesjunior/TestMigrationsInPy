import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_object(self):
        self.client['a'] = 'foo'
        self.assert_(isinstance(self.client.object('refcount', 'a'), int))
        self.assert_(isinstance(self.client.object('idletime', 'a'), int))
        self.assertEquals(self.client.object('encoding', 'a'), b('raw'))