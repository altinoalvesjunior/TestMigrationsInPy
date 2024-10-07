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
    def test_not_slice_like_arrays(self):
        def assert_not_slice_like(arr):
            assert not BlockPlacement(arr).is_slice_like

        assert_not_slice_like([])
        assert_not_slice_like([-1])
        assert_not_slice_like([-1, -2, -3])
        assert_not_slice_like([-10])
        assert_not_slice_like([-1])
        assert_not_slice_like([-1, 0, 1, 2])
        assert_not_slice_like([-2, 0, 2, 4])
        assert_not_slice_like([1, 0, -1])
        assert_not_slice_like([1, 1, 1])