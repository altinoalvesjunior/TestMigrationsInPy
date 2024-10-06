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
    def test_interleave(self):

        # self
        for dtype in ['f8', 'i8', 'object', 'bool', 'complex', 'M8[ns]',
                      'm8[ns]']:
            mgr = create_mgr('a: {0}'.format(dtype))
            assert mgr.as_matrix().dtype == dtype
            mgr = create_mgr('a: {0}; b: {0}'.format(dtype))
            assert mgr.as_matrix().dtype == dtype

        # will be converted according the actual dtype of the underlying
        mgr = create_mgr('a: category')
        assert mgr.as_matrix().dtype == 'i8'
        mgr = create_mgr('a: category; b: category')
        assert mgr.as_matrix().dtype == 'i8'
        mgr = create_mgr('a: category; b: category2')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: category2')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: category2; b: category2')
        assert mgr.as_matrix().dtype == 'object'

        # combinations
        mgr = create_mgr('a: f8')
        assert mgr.as_matrix().dtype == 'f8'
        mgr = create_mgr('a: f8; b: i8')
        assert mgr.as_matrix().dtype == 'f8'
        mgr = create_mgr('a: f4; b: i8')
        assert mgr.as_matrix().dtype == 'f8'
        mgr = create_mgr('a: f4; b: i8; d: object')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: bool; b: i8')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: complex')
        assert mgr.as_matrix().dtype == 'complex'
        mgr = create_mgr('a: f8; b: category')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: M8[ns]; b: category')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: M8[ns]; b: bool')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: M8[ns]; b: i8')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: m8[ns]; b: bool')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: m8[ns]; b: i8')
        assert mgr.as_matrix().dtype == 'object'
        mgr = create_mgr('a: M8[ns]; b: m8[ns]')
        assert mgr.as_matrix().dtype == 'object'