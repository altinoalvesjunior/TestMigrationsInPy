import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    def test_config_get(self):
        data = self.client.config_get()
        self.assert_('maxmemory' in data)
        self.assert_(data['maxmemory'].isdigit())