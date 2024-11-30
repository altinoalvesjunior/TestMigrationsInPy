import unittest
import datetime
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_lastsave(self):
        self.assert_(isinstance(self.client.lastsave(), datetime.datetime))