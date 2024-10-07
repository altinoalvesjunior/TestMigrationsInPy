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
     def test_intercept_astype_object(self):
        series = Series(date_range('1/1/2000', periods=10))

        # this test no longer makes sense as series is by default already
        # M8[ns]
        expected = series.astype('object')

        df = DataFrame({'a': series,
                        'b': np.random.randn(len(series))})
        exp_dtypes = Series([np.dtype('datetime64[ns]'),
                             np.dtype('float64')], index=['a', 'b'])
        tm.assert_series_equal(df.dtypes, exp_dtypes)

        result = df.values.squeeze()
        self.assertTrue((result[:, 0] == expected.values).all())

        df = DataFrame({'a': series, 'b': ['foo'] * len(series)})

        result = df.values.squeeze()
        self.assertTrue((result[:, 0] == expected.values).all())