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
    def test_astype_datetimes(self):
        import pandas._libs.tslib as tslib
        s = Series(tslib.iNaT, dtype='M8[ns]', index=lrange(5))
        s = s.astype('O')
        self.assertEqual(s.dtype, np.object_)

        s = Series([datetime(2001, 1, 2, 0, 0)])
        s = s.astype('O')
        self.assertEqual(s.dtype, np.object_)

        s = Series([datetime(2001, 1, 2, 0, 0) for i in range(3)])
        s[1] = np.nan
        self.assertEqual(s.dtype, 'M8[ns]')
        s = s.astype('O')
        self.assertEqual(s.dtype, np.object_)