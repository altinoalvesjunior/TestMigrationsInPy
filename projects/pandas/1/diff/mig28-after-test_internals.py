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
    def test_reindex_items(self):
        # mgr is not consolidated, f8 & f8-2 blocks
        mgr = create_mgr('a: f8; b: i8; c: f8; d: i8; e: f8;'
                         'f: bool; g: f8-2')

        reindexed = mgr.reindex_axis(['g', 'c', 'a', 'd'], axis=0)
        assert reindexed.nblocks == 2
        tm.assert_index_equal(reindexed.items, pd.Index(['g', 'c', 'a', 'd']))
        assert_almost_equal(
            mgr.get('g', fastpath=False), reindexed.get('g', fastpath=False))
        assert_almost_equal(
            mgr.get('c', fastpath=False), reindexed.get('c', fastpath=False))
        assert_almost_equal(
            mgr.get('a', fastpath=False), reindexed.get('a', fastpath=False))
        assert_almost_equal(
            mgr.get('d', fastpath=False), reindexed.get('d', fastpath=False))
        assert_almost_equal(
            mgr.get('g').internal_values(),
            reindexed.get('g').internal_values())
        assert_almost_equal(
            mgr.get('c').internal_values(),
            reindexed.get('c').internal_values())
        assert_almost_equal(
            mgr.get('a').internal_values(),
            reindexed.get('a').internal_values())
        assert_almost_equal(
            mgr.get('d').internal_values(),
            reindexed.get('d').internal_values())