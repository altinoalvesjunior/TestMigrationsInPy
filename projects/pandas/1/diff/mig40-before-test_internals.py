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
    def test_blockplacement_add(self):
        bpl = BlockPlacement(slice(0, 5))
        self.assertEqual(bpl.add(1).as_slice, slice(1, 6, 1))
        self.assertEqual(bpl.add(np.arange(5)).as_slice, slice(0, 10, 2))
        self.assertEqual(list(bpl.add(np.arange(5, 0, -1))), [5, 5, 5, 5, 5])