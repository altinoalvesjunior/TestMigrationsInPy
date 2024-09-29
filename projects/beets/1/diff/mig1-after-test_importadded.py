"""Tests for the `importadded` plugin."""

import os

import pytest

from beets.test.helper import AutotagStub, ImportTestCase, PluginMixin


class ImportAddedTest(PluginMixin, ImportTestCase):
    def assertEqualTimes(self, first, second, msg=None):  # noqa
        """For comparing file modification times at a sufficient precision"""
        assert first == pytest.approx(second, rel=1e-4), msg