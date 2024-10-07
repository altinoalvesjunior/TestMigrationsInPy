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
    def test_blockplacement_add_int(self):
        def assert_add_equals(val, inc, result):
            self.assertEqual(list(BlockPlacement(val).add(inc)), result)

        assert_add_equals(slice(0, 0), 0, [])
        assert_add_equals(slice(1, 4), 0, [1, 2, 3])
        assert_add_equals(slice(3, 0, -1), 0, [3, 2, 1])
        assert_add_equals(slice(2, None, -1), 0, [2, 1, 0])
        assert_add_equals([1, 2, 4], 0, [1, 2, 4])

        assert_add_equals(slice(0, 0), 10, [])
        assert_add_equals(slice(1, 4), 10, [11, 12, 13])
        assert_add_equals(slice(3, 0, -1), 10, [13, 12, 11])
        assert_add_equals(slice(2, None, -1), 10, [12, 11, 10])
        assert_add_equals([1, 2, 4], 10, [11, 12, 14])

        assert_add_equals(slice(0, 0), -1, [])
        assert_add_equals(slice(1, 4), -1, [0, 1, 2])
        assert_add_equals(slice(3, 0, -1), -1, [2, 1, 0])
        assert_add_equals([1, 2, 4], -1, [0, 1, 3])

        self.assertRaises(ValueError,
                          lambda: BlockPlacement(slice(1, 4)).add(-10))
        self.assertRaises(ValueError,
                          lambda: BlockPlacement([1, 2, 4]).add(-10))
        self.assertRaises(ValueError,
                          lambda: BlockPlacement(slice(2, None, -1)).add(-1))