import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_echo(self):
        self.assertEquals(self.client.echo('foo bar'), b('foo bar'))