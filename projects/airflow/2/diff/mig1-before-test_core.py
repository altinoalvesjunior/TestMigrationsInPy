import multiprocessing
import os
import signal
import unittest
from datetime import timedelta
from time import sleep

from dateutil.relativedelta import relativedelta
from airflow.utils.dates import infer_time_unit, round_time, scale_time_units
from airflow.utils.timezone import datetime

class TestCore(unittest.TestCase):
    def test_round_time(self):
        rt1 = round_time(datetime(2015, 1, 1, 6), timedelta(days=1))
        self.assertEqual(datetime(2015, 1, 1, 0, 0), rt1)
        rt2 = round_time(datetime(2015, 1, 2), relativedelta(months=1))
        self.assertEqual(datetime(2015, 1, 1, 0, 0), rt2)
        rt3 = round_time(datetime(2015, 9, 16, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 16, 0, 0), rt3)
        rt4 = round_time(datetime(2015, 9, 15, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 15, 0, 0), rt4)
        rt5 = round_time(datetime(2015, 9, 14, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 14, 0, 0), rt5)
        rt6 = round_time(datetime(2015, 9, 13, 0, 0), timedelta(1), datetime(2015, 9, 14, 0, 0))
        self.assertEqual(datetime(2015, 9, 14, 0, 0), rt6)