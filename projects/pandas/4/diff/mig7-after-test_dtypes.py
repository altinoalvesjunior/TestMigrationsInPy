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
    def test_astype_dict(self):
        # see gh-7271
        s = Series(range(0, 10, 2), name='abc')

        result = s.astype({'abc': str})
        expected = Series(['0', '2', '4', '6', '8'], name='abc')
        tm.assert_series_equal(result, expected)

        result = s.astype({'abc': 'float64'})
        expected = Series([0.0, 2.0, 4.0, 6.0, 8.0], dtype='float64',
                          name='abc')
        tm.assert_series_equal(result, expected)
        with pytest.raises(KeyError):
            s.astype({'abc': str, 'def': str})
        with pytest.raises(KeyError):
            s.astype({0: str})