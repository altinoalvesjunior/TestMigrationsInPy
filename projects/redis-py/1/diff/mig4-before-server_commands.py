import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_binary_get_set(self):
        self.assertTrue(self.client.set(' foo bar ', '123'))
        self.assertEqual(self.client.get(' foo bar '), b('123'))
        self.assertTrue(self.client.set(' foo\r\nbar\r\n ', '456'))
        self.assertEqual(self.client.get(' foo\r\nbar\r\n '), b('456'))
        self.assertTrue(self.client.set(' \r\n\t\x07\x13 ', '789'))
        self.assertEqual(self.client.get(' \r\n\t\x07\x13 '), b('789'))
        self.assertEqual(
            sorted(self.client.keys('*')),
            [b(' \r\n\t\x07\x13 '), b(' foo\r\nbar\r\n '), b(' foo bar ')])
        self.assertTrue(self.client.delete(' foo bar '))
        self.assertTrue(self.client.delete(' foo\r\nbar\r\n '))
        self.assertTrue(self.client.delete(' \r\n\t\x07\x13 '))