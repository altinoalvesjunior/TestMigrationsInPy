import multiprocessing
import os
import signal
import unittest
from datetime import timedelta
from time import sleep

from dateutil.relativedelta import relativedelta
from numpy.testing import assert_array_almost_equal
from airflow.utils.dates import infer_time_unit, round_time, scale_time_units

class TestCore(unittest.TestCase):
    def test_scale_time_units(self):
        # use assert_almost_equal from numpy.testing since we are comparing
        # floating point arrays
        arr1 = scale_time_units([130, 5400, 10], 'minutes')
        assert_array_almost_equal(arr1, [2.167, 90.0, 0.167], decimal=3)
        arr2 = scale_time_units([110, 50, 10, 100], 'seconds')
        assert_array_almost_equal(arr2, [110.0, 50.0, 10.0, 100.0], decimal=3)
        arr3 = scale_time_units([100000, 50000, 10000, 20000], 'hours')
        assert_array_almost_equal(arr3, [27.778, 13.889, 2.778, 5.556], decimal=3)
        arr4 = scale_time_units([200000, 100000], 'days')
        assert_array_almost_equal(arr4, [2.315, 1.157], decimal=3)