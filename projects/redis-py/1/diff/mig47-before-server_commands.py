import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_setrange(self):
        self.assertEquals(self.client.setrange('a', 5, 'abcdef'), 11)
        self.assertEquals(self.client['a'], b('\0\0\0\0\0abcdef'))
        self.client['a'] = 'Hello World'
        self.assertEquals(self.client.setrange('a', 6, 'Redis'), 11)
        self.assertEquals(self.client['a'], b('Hello Redis'))