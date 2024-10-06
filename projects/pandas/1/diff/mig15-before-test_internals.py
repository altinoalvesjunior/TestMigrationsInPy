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

class TestBlockManager(tm.TestCase):
    def test_set_change_dtype_slice(self):  # GH8850
        cols = MultiIndex.from_tuples([('1st', 'a'), ('2nd', 'b'), ('3rd', 'c')
                                       ])
        df = DataFrame([[1.0, 2, 3], [4.0, 5, 6]], columns=cols)
        df['2nd'] = df['2nd'] * 2.0

        self.assertEqual(sorted(df.blocks.keys()), ['float64', 'int64'])
        assert_frame_equal(df.blocks['float64'], DataFrame(
            [[1.0, 4.0], [4.0, 10.0]], columns=cols[:2]))
        assert_frame_equal(df.blocks['int64'], DataFrame(
            [[3], [6]], columns=cols[2:]))