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
    def test_get_scalar(self):
        for item in self.mgr.items:
            for i, index in enumerate(self.mgr.axes[1]):
                res = self.mgr.get_scalar((item, index))
                exp = self.mgr.get(item, fastpath=False)[i]
                self.assertEqual(res, exp)
                exp = self.mgr.get(item).internal_values()[i]
                self.assertEqual(res, exp)