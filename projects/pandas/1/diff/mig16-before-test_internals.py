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
    def test_copy(self):
        cp = self.mgr.copy(deep=False)
        for blk, cp_blk in zip(self.mgr.blocks, cp.blocks):

            # view assertion
            self.assertTrue(cp_blk.equals(blk))
            self.assertTrue(cp_blk.values.base is blk.values.base)

        cp = self.mgr.copy(deep=True)
        for blk, cp_blk in zip(self.mgr.blocks, cp.blocks):

            # copy assertion we either have a None for a base or in case of
            # some blocks it is an array (e.g. datetimetz), but was copied
            self.assertTrue(cp_blk.equals(blk))
            if cp_blk.values.base is not None and blk.values.base is not None:
                self.assertFalse(cp_blk.values.base is blk.values.base)
            else:
                self.assertTrue(cp_blk.values.base is None and blk.values.base
                                is None)