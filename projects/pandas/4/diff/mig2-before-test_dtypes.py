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
    def test_dtype(self):

        self.assertEqual(self.ts.dtype, np.dtype('float64'))
        self.assertEqual(self.ts.dtypes, np.dtype('float64'))
        self.assertEqual(self.ts.ftype, 'float64:dense')
        self.assertEqual(self.ts.ftypes, 'float64:dense')
        assert_series_equal(self.ts.get_dtype_counts(), Series(1, ['float64']))
        assert_series_equal(self.ts.get_ftype_counts(), Series(
            1, ['float64:dense']))