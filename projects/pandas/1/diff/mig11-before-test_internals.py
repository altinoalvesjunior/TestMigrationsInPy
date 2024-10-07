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
    def test_is_indexed_like(self):
        mgr1 = create_mgr('a,b: f8')
        mgr2 = create_mgr('a:i8; b:bool')
        mgr3 = create_mgr('a,b,c: f8')
        self.assertTrue(mgr1._is_indexed_like(mgr1))
        self.assertTrue(mgr1._is_indexed_like(mgr2))
        self.assertTrue(mgr1._is_indexed_like(mgr3))

        self.assertFalse(mgr1._is_indexed_like(mgr1.get_slice(
            slice(-1), axis=1)))