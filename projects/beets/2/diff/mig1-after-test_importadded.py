"""Tests for the `importadded` plugin."""

import os

import pytest

from beets.test.helper import AutotagStub, ImportTestCase, PluginMixin


class ImportAddedTest(PluginMixin, ImportTestCase):
    # The minimum mtime of the files to be imported
    plugin = "importadded"
    min_mtime = None
    
    def assertEqualTimes(self, first, second, msg=None):  # noqa
        """For comparing file modification times at a sufficient precision"""
        assert first == pytest.approx(second, rel=1e-4), msg