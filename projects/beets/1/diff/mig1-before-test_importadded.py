import os

from beets.test.helper import AutotagStub, ImportTestCase, PluginMixin


class ImportAddedTest(PluginMixin, ImportTestCase):        
    def assertEqualTimes(self, first, second, msg=None):  # noqa
        """For comparing file modification times at a sufficient precision"""
        self.assertAlmostEqual(first, second, places=4, msg=msg)
