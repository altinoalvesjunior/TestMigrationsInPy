import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_get_set_bit(self):
        self.assertEquals(self.client.getbit('a', 5), False)
        self.assertEquals(self.client.setbit('a', 5, True), False)
        self.assertEquals(self.client.getbit('a', 5), True)
        self.assertEquals(self.client.setbit('a', 4, False), False)
        self.assertEquals(self.client.getbit('a', 4), False)
        self.assertEquals(self.client.setbit('a', 4, True), False)
        self.assertEquals(self.client.setbit('a', 5, True), True)
        self.assertEquals(self.client.getbit('a', 4), True)
        self.assertEquals(self.client.getbit('a', 5), True)