"""Test for dbcore's date-based queries.
"""

import time
import unittest
from datetime import datetime, timedelta

from beets.dbcore.query import (
    DateInterval,
    DateQuery,
    InvalidQueryArgumentValueError,
    _parse_periods,
)
from beets.test.helper import ItemInDBTestCase

class DateQueryConstructTest(unittest.TestCase):
    def test_too_many_components(self):
            with self.assertRaises(InvalidQueryArgumentValueError):
                DateQuery("added", "12-34-56-78")