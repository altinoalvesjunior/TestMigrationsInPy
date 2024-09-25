import os

from beets.test.helper import AutotagStub, ImportTestCase, PluginMixin
from beetsplug.importadded import ImportAddedPlugin


class ImportAddedTest(PluginMixin, ImportTestCase):
    # The minimum mtime of the files to be imported
    plugin = "importadded"
    min_mtime = None
        
    def assertEqualTimes(self, first, second, msg=None):  # noqa
        """For comparing file modification times at a sufficient precision"""
        self.assertAlmostEqual(first, second, places=4, msg=msg)
