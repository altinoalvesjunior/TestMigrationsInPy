import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_renamenx(self):
        self.client['a'] = '1'
        self.client['b'] = '2'
        self.assert_(not self.client.renamenx('a', 'b'))
        self.assertEquals(self.client['a'], b('1'))
        self.assertEquals(self.client['b'], b('2'))