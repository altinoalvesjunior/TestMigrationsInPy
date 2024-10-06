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
    @pytest.mark.parametrize("dtype", [int, np.int8, np.int64])
    def test_astype_cast_object_int_fail(self, dtype):
        arr = Series(["car", "house", "tree", "1"])
        with pytest.raises(ValueError):
            arr.astype(dtype)

    def test_astype_cast_object_int(self):
        arr = Series(['1', '2', '3', '4'], dtype=object)
        result = arr.astype(int)
        tm.assert_series_equal(result, Series(np.arange(1, 5)))