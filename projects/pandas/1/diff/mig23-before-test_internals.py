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
    def test_astype(self):
        # coerce all
        mgr = create_mgr('c: f4; d: f2; e: f8')
        for t in ['float16', 'float32', 'float64', 'int32', 'int64']:
            t = np.dtype(t)
            tmgr = mgr.astype(t)
            self.assertEqual(tmgr.get('c').dtype.type, t)
            self.assertEqual(tmgr.get('d').dtype.type, t)
            self.assertEqual(tmgr.get('e').dtype.type, t)

        # mixed
        mgr = create_mgr('a,b: object; c: bool; d: datetime;'
                         'e: f4; f: f2; g: f8')
        for t in ['float16', 'float32', 'float64', 'int32', 'int64']:
            t = np.dtype(t)
            tmgr = mgr.astype(t, errors='ignore')
            self.assertEqual(tmgr.get('c').dtype.type, t)
            self.assertEqual(tmgr.get('e').dtype.type, t)
            self.assertEqual(tmgr.get('f').dtype.type, t)
            self.assertEqual(tmgr.get('g').dtype.type, t)

            self.assertEqual(tmgr.get('a').dtype.type, np.object_)
            self.assertEqual(tmgr.get('b').dtype.type, np.object_)
            if t != np.int64:
                self.assertEqual(tmgr.get('d').dtype.type, np.datetime64)
            else:
                self.assertEqual(tmgr.get('d').dtype.type, t)