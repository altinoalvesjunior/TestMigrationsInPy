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
    @pytest.mark.parametrize("dtype", [compat.text_type, np.str_])
    @pytest.mark.parametrize("series", [Series([string.digits * 10,
                                                tm.rands(63),
                                                tm.rands(64),
                                                tm.rands(1000)]),
                                        Series([string.digits * 10,
                                                tm.rands(63),
                                                tm.rands(64), nan, 1.0])])
    def test_astype_str_map(self, dtype, series):
        # see gh-4405
        result = series.astype(dtype)
        expected = series.map(compat.text_type)
        tm.assert_series_equal(result, expected)
    @pytest.mark.parametrize("dtype", [str, compat.text_type])
    def test_astype_str_cast(self, dtype):
        # see gh-9757: test str and unicode on python 2.x
        # and just str on python 3.x
        ts = Series([Timestamp('2010-01-04 00:00:00')])
        s = ts.astype(dtype)
        expected = Series([dtype('2010-01-04')])
        tm.assert_series_equal(s, expected)
        ts = Series([Timestamp('2010-01-04 00:00:00', tz='US/Eastern')])
        s = ts.astype(dtype)
        expected = Series([dtype('2010-01-04 00:00:00-05:00')])
        tm.assert_series_equal(s, expected)
        td = Series([Timedelta(1, unit='d')])
        s = td.astype(dtype)
        expected = Series([dtype('1 days 00:00:00.000000000')])
        tm.assert_series_equal(s, expected)