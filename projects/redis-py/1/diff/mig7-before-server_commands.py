import unittest
import redis

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client - igual ao mig1-before) ...

    def test_delitem(self):
        self.client['a'] = 'foo'
        del self.client['a']
        self.assertEquals(self.client.get('a'), None)