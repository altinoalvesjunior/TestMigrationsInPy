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
    def test_astype_str(self):
        # GH4405
        digits = string.digits
        s1 = Series([digits * 10, tm.rands(63), tm.rands(64), tm.rands(1000)])
        s2 = Series([digits * 10, tm.rands(63), tm.rands(64), nan, 1.0])
        types = (compat.text_type, np.str_)
        for typ in types:
            for s in (s1, s2):
                res = s.astype(typ)
                expec = s.map(compat.text_type)
                assert_series_equal(res, expec)
        # GH9757
        # Test str and unicode on python 2.x and just str on python 3.x
        for tt in set([str, compat.text_type]):
            ts = Series([Timestamp('2010-01-04 00:00:00')])
            s = ts.astype(tt)
            expected = Series([tt('2010-01-04')])
            assert_series_equal(s, expected)
            ts = Series([Timestamp('2010-01-04 00:00:00', tz='US/Eastern')])
            s = ts.astype(tt)
            expected = Series([tt('2010-01-04 00:00:00-05:00')])
            assert_series_equal(s, expected)
            td = Series([Timedelta(1, unit='d')])
            s = td.astype(tt)
            expected = Series([tt('1 days 00:00:00.000000000')])
            assert_series_equal(s, expected)
