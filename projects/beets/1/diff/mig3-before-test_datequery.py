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
    def test_invalid_date_query(self):
            q_list = [
                "2001-01-0a",
                "2001-0a",
                "200a",
                "2001-01-01..2001-01-0a",
                "2001-0a..2001-01",
                "200a..2002",
                "20aa..",
                "..2aa",
            ]
            for q in q_list:
                with self.assertRaises(InvalidQueryArgumentValueError):
                    DateQuery("added", q)