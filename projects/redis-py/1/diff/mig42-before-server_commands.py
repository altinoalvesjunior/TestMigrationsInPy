import unittest
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    def test_set_nx(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.12'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return
        self.assertEquals(self.client.set('foo', '1', nx=True), True)
        self.assertEquals(self.client.set('foo', '2', nx=True), None)
        self.assertEquals(self.client.get('foo'), b('1'))