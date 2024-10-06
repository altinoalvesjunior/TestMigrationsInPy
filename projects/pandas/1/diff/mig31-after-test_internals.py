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
    def test_equals_block_order_different_dtypes(self):
        # GH 9330

        mgr_strings = [
            "a:i8;b:f8",  # basic case
            "a:i8;b:f8;c:c8;d:b",  # many types
            "a:i8;e:dt;f:td;g:string",  # more types
            "a:i8;b:category;c:category2;d:category2",  # categories
            "c:sparse;d:sparse_na;b:f8",  # sparse
        ]

        for mgr_string in mgr_strings:
            bm = create_mgr(mgr_string)
            block_perms = itertools.permutations(bm.blocks)
            for bm_perm in block_perms:
                bm_this = BlockManager(bm_perm, bm.axes)
                assert bm.equals(bm_this)
                assert bm_this.equals(bm)