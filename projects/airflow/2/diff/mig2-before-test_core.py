import multiprocessing
import os
import signal
import unittest
from datetime import timedelta
from time import sleep

from airflow.utils.dates import infer_time_unit, round_time, scale_time_units
from airflow.utils.timezone import datetime

DEV_NULL = '/dev/null'
DEFAULT_DATE = datetime(2015, 1, 1)
TEST_DAG_ID = 'unit_tests'

class TestCore(unittest.TestCase):
    def test_infer_time_unit(self):
        self.assertEqual('minutes', infer_time_unit([130, 5400, 10]))
        self.assertEqual('seconds', infer_time_unit([110, 50, 10, 100]))
        self.assertEqual('hours', infer_time_unit([100000, 50000, 10000, 20000]))
        self.assertEqual('days', infer_time_unit([200000, 100000]))