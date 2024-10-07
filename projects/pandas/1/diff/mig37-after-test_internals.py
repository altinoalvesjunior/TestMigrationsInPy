from datetime import datetime, date

import pytest
import numpy as np

import re
import itertools
from pandas import (Index, MultiIndex, DataFrame, DatetimeIndex,
                    Series, Categorical)
from pandas.compat import OrderedDict, lrange
from pandas.sparse.array import SparseArray
from pandas.core.internals import (BlockPlacement, SingleBlockManager,
                                   make_block, BlockManager)
import pandas.core.algorithms as algos
import pandas.util.testing as tm
import pandas as pd
from pandas._libs import lib
from pandas.util.testing import (assert_almost_equal, assert_frame_equal,
                                 randn, assert_series_equal)
from pandas.compat import zip, u

class TestBlockPlacement(tm.TestCase):
    def test_array_to_slice_conversion(self):
        def assert_as_slice_equals(arr, slc):
            assert BlockPlacement(arr).as_slice == slc

        assert_as_slice_equals([0], slice(0, 1, 1))
        assert_as_slice_equals([100], slice(100, 101, 1))

        assert_as_slice_equals([0, 1, 2], slice(0, 3, 1))
        assert_as_slice_equals([0, 5, 10], slice(0, 15, 5))
        assert_as_slice_equals([0, 100], slice(0, 200, 100))

        assert_as_slice_equals([2, 1], slice(2, 0, -1))
        assert_as_slice_equals([2, 1, 0], slice(2, None, -1))
        assert_as_slice_equals([100, 0], slice(100, None, -100))