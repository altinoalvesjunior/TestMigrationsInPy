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
    def test_consolidate_ordering_issues(self):
        self.mgr.set('f', randn(N))
        self.mgr.set('d', randn(N))
        self.mgr.set('b', randn(N))
        self.mgr.set('g', randn(N))
        self.mgr.set('h', randn(N))
        # we have datetime/tz blocks in self.mgr
        cons = self.mgr.consolidate()
        self.assertEqual(cons.nblocks, 4)
        cons = self.mgr.consolidate().get_numeric_data()
        self.assertEqual(cons.nblocks, 1)
        tm.assertIsInstance(cons.blocks[0].mgr_locs, lib.BlockPlacement)