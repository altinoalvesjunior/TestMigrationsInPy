import unittest
from datetime import datetime, timedelta

import pendulum
from dateutil.relativedelta import relativedelta
from pytest import approx

from airflow.utils import dates, timezone

class TestDates(unittest.TestCase):
    def test_scale_time_units(self):
        # floating point arrays
        arr1 = dates.scale_time_units([130, 5400, 10], 'minutes')
        assert arr1 == approx([2.1667, 90.0, 0.1667], rel=1e-3)
        arr2 = dates.scale_time_units([110, 50, 10, 100], 'seconds')
        assert arr2 == approx([110.0, 50.0, 10.0, 100.0])
        arr3 = dates.scale_time_units([100000, 50000, 10000, 20000], 'hours')
        assert arr3 == approx([27.7778, 13.8889, 2.7778, 5.5556], rel=1e-3)
        arr4 = dates.scale_time_units([200000, 100000], 'days')
        assert arr4 == approx([2.3147, 1.1574], rel=1e-3)