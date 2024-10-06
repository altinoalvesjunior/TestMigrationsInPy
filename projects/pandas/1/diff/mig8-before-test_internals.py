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

class TestDatetimeBlock(tm.TestCase):

    def test_try_coerce_arg(self):
        block = create_block('datetime', [0])

        # coerce None
        none_coerced = block._try_coerce_args(block.values, None)[2]
        self.assertTrue(pd.Timestamp(none_coerced) is pd.NaT)

        # coerce different types of date bojects
        vals = (np.datetime64('2010-10-10'), datetime(2010, 10, 10),
                date(2010, 10, 10))
        for val in vals:
            coerced = block._try_coerce_args(block.values, val)[2]
            self.assertEqual(np.int64, type(coerced))
            self.assertEqual(pd.Timestamp('2010-10-10'), pd.Timestamp(coerced))