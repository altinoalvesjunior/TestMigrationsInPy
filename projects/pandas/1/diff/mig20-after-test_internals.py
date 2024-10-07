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
    def test_as_matrix_int_bool(self):
        mgr = create_mgr('a: bool-1; b: bool-2')
        assert mgr.as_matrix().dtype == np.bool_

        mgr = create_mgr('a: i8-1; b: i8-2; c: i4; d: i2; e: u1')
        assert mgr.as_matrix().dtype == np.int64

        mgr = create_mgr('c: i4; d: i2; e: u1')
        assert mgr.as_matrix().dtype == np.int32