import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_rename(self):
        self.client['a'] = '1'
        self.assert_(self.client.rename('a', 'b'))
        self.assertEquals(self.client.get('a'), None)
        self.assertEquals(self.client['b'], b('1'))