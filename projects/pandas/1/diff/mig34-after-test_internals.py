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

class TestBlockPlacement(tm.TestCase):

    def test_slice_len(self):
        assert len(BlockPlacement(slice(0, 4))) == 4
        assert len(BlockPlacement(slice(0, 4, 2))) == 2
        assert len(BlockPlacement(slice(0, 3, 2))) == 2

        assert len(BlockPlacement(slice(0, 1, 2))) == 1
        assert len(BlockPlacement(slice(1, 0, -1))) == 1