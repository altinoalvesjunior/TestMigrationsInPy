# coding=utf-8
# pylint: disable-msg=E1101,W0612

import sys
from datetime import datetime
import string

from numpy import nan
import numpy as np

from pandas import Series, Timestamp, Timedelta, DataFrame, date_range

from pandas.compat import lrange, range, u
from pandas import compat
from pandas.util.testing import assert_series_equal
import pandas.util.testing as tm

from .common import TestData


class TestSeriesDtypes(TestData, tm.TestCase):
     def test_arg_for_errors_in_astype(self):
        # issue #14878
        sr = Series([1, 2, 3])

        with self.assertRaises(ValueError):
            sr.astype(np.float64, errors=False)

        with tm.assert_produces_warning(FutureWarning):
            sr.astype(np.int8, raise_on_error=True)

        sr.astype(np.int8, errors='raise')