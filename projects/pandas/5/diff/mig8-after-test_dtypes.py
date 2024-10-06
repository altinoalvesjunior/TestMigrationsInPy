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
    def test_arg_for_errors_in_astype(self):
        # see gh-14878
        s = Series([1, 2, 3])

        with pytest.raises(ValueError):
            s.astype(np.float64, errors=False)

        with tm.assert_produces_warning(FutureWarning):
            s.astype(np.int8, raise_on_error=True)

        s.astype(np.int8, errors='raise')