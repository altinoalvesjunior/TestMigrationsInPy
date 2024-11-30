import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_info(self):
        self.client['a'] = 'foo'
        self.client['b'] = 'bar'
        info = self.client.info()
        self.assert_(isinstance(info, dict))
        self.assertEquals(info['db9']['keys'], 2)