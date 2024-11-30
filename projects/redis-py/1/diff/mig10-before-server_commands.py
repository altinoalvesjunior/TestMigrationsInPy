import unittest
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_client_setname(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.9'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return
        self.assert_(self.client.client_setname('redis_py_test'))
        self.assertEquals(
            self.client.client_getname(),
            'redis_py_test'
        )