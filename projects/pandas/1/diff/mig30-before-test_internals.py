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
    def test_equals(self):
        # unique items
        bm1 = create_mgr('a,b,c: i8-1; d,e,f: i8-2')
        bm2 = BlockManager(bm1.blocks[::-1], bm1.axes)
        self.assertTrue(bm1.equals(bm2))

        bm1 = create_mgr('a,a,a: i8-1; b,b,b: i8-2')
        bm2 = BlockManager(bm1.blocks[::-1], bm1.axes)
        self.assertTrue(bm1.equals(bm2))