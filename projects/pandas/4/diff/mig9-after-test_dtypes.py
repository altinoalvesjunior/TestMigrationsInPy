# coding=utf-8
# pylint: disable-msg=E1101,W0612

import pytest
from datetime import datetime
import sys
import string
import warnings

from numpy import nan
import numpy as np

from pandas import Series, Timestamp, Timedelta, DataFrame, date_range

from pandas.compat import lrange, range, u
from pandas import compat
import pandas.util.testing as tm

from .common import TestData


class TestSeriesDtypes(TestData):
    def test_intercept_astype_object(self):
        series = Series(date_range('1/1/2000', periods=10))

        # This test no longer makes sense, as
        # Series is by default already M8[ns].
        expected = series.astype('object')

        df = DataFrame({'a': series,
                        'b': np.random.randn(len(series))})
        exp_dtypes = Series([np.dtype('datetime64[ns]'),
                             np.dtype('float64')], index=['a', 'b'])
        tm.assert_series_equal(df.dtypes, exp_dtypes)

        result = df.values.squeeze()
        assert (result[:, 0] == expected.values).all()

        df = DataFrame({'a': series, 'b': ['foo'] * len(series)})

        result = df.values.squeeze()
        assert (result[:, 0] == expected.values).all()