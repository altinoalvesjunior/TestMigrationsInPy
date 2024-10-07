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
    def test_as_matrix_datetime_tz(self):
        mgr = create_mgr('h: M8[ns, US/Eastern]; g: M8[ns, CET]')
        self.assertEqual(mgr.get('h').dtype, 'datetime64[ns, US/Eastern]')
        self.assertEqual(mgr.get('g').dtype, 'datetime64[ns, CET]')
        self.assertEqual(mgr.as_matrix().dtype, 'object')