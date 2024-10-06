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

class TestBlockManager(object):
    def test_consolidate_ordering_issues(self, mgr):
        mgr.set('f', randn(N))
        mgr.set('d', randn(N))
        mgr.set('b', randn(N))
        mgr.set('g', randn(N))
        mgr.set('h', randn(N))
        # we have datetime/tz blocks in mgr
        cons = mgr.consolidate()
        assert cons.nblocks == 4
        cons = mgr.consolidate().get_numeric_data()
        assert cons.nblocks == 1
        assert isinstance(cons.blocks[0].mgr_locs, lib.BlockPlacement)