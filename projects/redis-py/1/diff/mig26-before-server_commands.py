import unittest
import datetime
import time
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_pexpireat(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        expire_at = datetime.datetime.now() + datetime.timedelta(minutes=1)
        self.assertEquals(self.client.pexpireat('a', expire_at), False)
        self.client['a'] = 'foo'
        # expire at in unix time (milliseconds)
        expire_at_seconds = int(time.mktime(expire_at.timetuple())) * 1000
        self.assertEquals(self.client.pexpireat('a', expire_at_seconds), True)
        self.assert_(self.client.ttl('a') <= 60)  # Valor aproximado
        # expire at given a datetime object
        self.client['b'] = 'bar'
        self.assertEquals(self.client.pexpireat('b', expire_at), True)
        self.assert_(self.client.ttl('b') <= 60)  # Valor aproximado