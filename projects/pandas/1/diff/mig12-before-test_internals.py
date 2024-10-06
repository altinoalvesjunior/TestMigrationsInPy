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
    def test_duplicate_ref_loc_failure(self):
        tmp_mgr = create_mgr('a:bool; a: f8')

        axes, blocks = tmp_mgr.axes, tmp_mgr.blocks

        blocks[0].mgr_locs = np.array([0])
        blocks[1].mgr_locs = np.array([0])
        # test trying to create block manager with overlapping ref locs
        self.assertRaises(AssertionError, BlockManager, blocks, axes)

        blocks[0].mgr_locs = np.array([0])
        blocks[1].mgr_locs = np.array([1])
        mgr = BlockManager(blocks, axes)
        mgr.iget(1)