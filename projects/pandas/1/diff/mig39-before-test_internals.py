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
    def test_slice_iter(self):
        self.assertEqual(list(BlockPlacement(slice(0, 3))), [0, 1, 2])
        self.assertEqual(list(BlockPlacement(slice(0, 0))), [])
        self.assertEqual(list(BlockPlacement(slice(3, 0))), [])

        self.assertEqual(list(BlockPlacement(slice(3, 0, -1))), [3, 2, 1])
        self.assertEqual(list(BlockPlacement(slice(3, None, -1))),
                         [3, 2, 1, 0])