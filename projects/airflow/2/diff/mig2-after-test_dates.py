import unittest
from datetime import datetime, timedelta

import pendulum
from dateutil.relativedelta import relativedelta
from pytest import approx

from airflow.utils import dates, timezone

class TestDates(unittest.TestCase):
    def test_infer_time_unit(self):
        assert dates.infer_time_unit([130, 5400, 10]) == 'minutes'
        assert dates.infer_time_unit([110, 50, 10, 100]) == 'seconds'
        assert dates.infer_time_unit([100000, 50000, 10000, 20000]) == 'hours'
        assert dates.infer_time_unit([200000, 100000]) == 'days'