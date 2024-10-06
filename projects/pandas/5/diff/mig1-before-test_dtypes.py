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

    def test_astype(self):
        s = Series(np.random.randn(5), name='foo')

        for dtype in ['float32', 'float64', 'int64', 'int32']:
            astyped = s.astype(dtype)
            self.assertEqual(astyped.dtype, dtype)
            self.assertEqual(astyped.name, s.name)