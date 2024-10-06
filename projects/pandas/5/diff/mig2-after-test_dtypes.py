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
    def test_dtype(self):

        assert self.ts.dtype == np.dtype('float64')
        assert self.ts.dtypes == np.dtype('float64')
        assert self.ts.ftype == 'float64:dense'
        assert self.ts.ftypes == 'float64:dense'
        tm.assert_series_equal(self.ts.get_dtype_counts(),
                               Series(1, ['float64']))
        tm.assert_series_equal(self.ts.get_ftype_counts(),
                               Series(1, ['float64:dense']))