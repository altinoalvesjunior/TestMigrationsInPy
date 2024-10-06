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
    def test_astype_cast_nan_inf_int(self):
        # GH14265, check nan and inf raise error when converting to int
        types = [np.int32, np.int64]
        values = [np.nan, np.inf]
        msg = 'Cannot convert non-finite values \\(NA or inf\\) to integer'

        for this_type in types:
            for this_val in values:
                s = Series([this_val])
                with self.assertRaisesRegexp(ValueError, msg):
                    s.astype(this_type)