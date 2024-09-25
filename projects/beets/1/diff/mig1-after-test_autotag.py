"""Tests for autotagging functionality.
"""

import re
import unittest

import pytest
from beets import autotag, config
from beets.autotag import AlbumInfo, TrackInfo, match
from beets.autotag.hooks import Distance, string_dist
from beets.library import Item
from beets.test.helper import BeetsTestCase
from beets.util import plurality


class PluralityTest(BeetsTestCase):
    def test_plurality_empty_sequence_raises_error(self):
        with pytest.raises(ValueError):
            plurality([])