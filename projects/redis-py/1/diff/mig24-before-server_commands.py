import unittest
import datetime
import time
import redis

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client - igual ao mig1-before) ...

    def test_expireat(self):
        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.assertEquals(self.client.expireat('a', expire_at), False)
        self.client['a'] = 'foo'
        # expire at in unix time
        expire_at_seconds = int(time.mktime(expire_at.timetuple()))
        self.assertEquals(self.client.expireat('a', expire_at_seconds), True)
        self.assertEquals(self.client.ttl('a'), 60)  # Valor aproximado
        # expire at given a datetime object
        self.client['b'] = 'bar'
        self.assertEquals(self.client.expireat('b', expire_at), True)
        self.assertEquals(self.client.ttl('b'), 60)  # Valor aproximado