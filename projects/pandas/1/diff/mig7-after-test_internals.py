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

class TestBlock(tm.TestCase):

    def setUp(self):
        # self.fblock = get_float_ex()  # a,c,e
        # self.cblock = get_complex_ex() #
        # self.oblock = get_obj_ex()
        # self.bool_block = get_bool_ex()
        # self.int_block = get_int_ex()

        self.fblock = create_block('float', [0, 2, 4])
        self.cblock = create_block('complex', [7])
        self.oblock = create_block('object', [1, 3])
        self.bool_block = create_block('bool', [5])
        self.int_block = create_block('int', [6])
    
    def test_split_block_at(self):

        # with dup column support this method was taken out
        # GH3679
        pytest.skip("skipping for now")

        bs = list(self.fblock.split_block_at('a'))
        assert len(bs) == 1
        assert np.array_equal(bs[0].items, ['c', 'e'])

        bs = list(self.fblock.split_block_at('c'))
        assert len(bs) == 2
        assert np.array_equal(bs[0].items, ['a'])
        assert np.array_equal(bs[1].items, ['e'])

        bs = list(self.fblock.split_block_at('e'))
        assert len(bs) == 1
        assert np.array_equal(bs[0].items, ['a', 'c'])

        # bblock = get_bool_ex(['f'])
        # bs = list(bblock.split_block_at('f'))
        # assert len(bs), 0)