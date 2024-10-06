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

    @pytest.mark.parametrize("dtype", ["float32", "float64",
                                       "int64", "int32"])
    def test_astype(self, dtype):
        s = Series(np.random.randn(5), name='foo')
        as_typed = s.astype(dtype)

        assert as_typed.dtype == dtype
        assert as_typed.name == s.name