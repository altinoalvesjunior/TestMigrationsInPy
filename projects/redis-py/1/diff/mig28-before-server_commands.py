import unittest
import redis
from distutils.version import StrictVersion

class ServerCommandsTestCase(unittest.TestCase):
    # ... (setUp, tearDown, get_client - igual ao mig1-before) ...

    def test_bitcount(self):
        version = self.client.info()['redis_version']
        if StrictVersion(version) < StrictVersion('2.6.0'):
            try:
                raise unittest.SkipTest()
            except AttributeError:
                return

        self.client.setbit('a', 5, True)
        self.assertEquals(self.client.bitcount('a'), 1)
        self.client.setbit('a', 6, True)
        self.assertEquals(self.client.bitcount('a'), 2)
        self.client.setbit('a', 5, False)
        self.assertEquals(self.client.bitcount('a'), 1)
        self.client.setbit('a', 9, True)
        self.client.setbit('a', 17, True)
        self.client.setbit('a', 25, True)
        self.client.setbit('a', 33, True)
        self.assertEquals(self.client.bitcount('a'), 5)
        self.assertEquals(self.client.bitcount('a', 0, -1), 5)
        self.assertEquals(self.client.bitcount('a', 2, 3), 2)
        self.assertEquals(self.client.bitcount('a', -2, -1), 2)
        self.assertEquals(self.client.bitcount('a', 1, 1), 1)