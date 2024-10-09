import unittest
from datetime import datetime, timedelta

import pendulum
from dateutil.relativedelta import relativedelta
from pytest import approx

from airflow.utils import dates, timezone

class TestDates(unittest.TestCase):
    def test_round_time(self):
        rt1 = dates.round_time(timezone.datetime(2015, 1, 1, 6), timedelta(days=1))
        assert timezone.datetime(2015, 1, 1, 0, 0) == rt1
        rt2 = dates.round_time(timezone.datetime(2015, 1, 2), relativedelta(months=1))
        assert timezone.datetime(2015, 1, 1, 0, 0) == rt2
        rt3 = dates.round_time(
            timezone.datetime(2015, 9, 16, 0, 0), timedelta(1), timezone.datetime(2015, 9, 14, 0, 0)
        )
        assert timezone.datetime(2015, 9, 16, 0, 0) == rt3
        rt4 = dates.round_time(
            timezone.datetime(2015, 9, 15, 0, 0), timedelta(1), timezone.datetime(2015, 9, 14, 0, 0)
        )
        assert timezone.datetime(2015, 9, 15, 0, 0) == rt4
        rt5 = dates.round_time(
            timezone.datetime(2015, 9, 14, 0, 0), timedelta(1), timezone.datetime(2015, 9, 14, 0, 0)
        )
        assert timezone.datetime(2015, 9, 14, 0, 0) == rt5
        rt6 = dates.round_time(
            timezone.datetime(2015, 9, 13, 0, 0), timedelta(1), timezone.datetime(2015, 9, 14, 0, 0)
        )
        assert timezone.datetime(2015, 9, 14, 0, 0) == rt6
    def test_infer_time_unit(self):
        assert dates.infer_time_unit([130, 5400, 10]) == 'minutes'
        assert dates.infer_time_unit([110, 50, 10, 100]) == 'seconds'
        assert dates.infer_time_unit([100000, 50000, 10000, 20000]) == 'hours'
        assert dates.infer_time_unit([200000, 100000]) == 'days'