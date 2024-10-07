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
    def test_interleave_non_unique_cols(self):
        df = DataFrame([
            [pd.Timestamp('20130101'), 3.5],
            [pd.Timestamp('20130102'), 4.5]],
            columns=['x', 'x'],
            index=[1, 2])

        df_unique = df.copy()
        df_unique.columns = ['x', 'y']
        assert df_unique.values.shape == df.values.shape
        tm.assert_numpy_array_equal(df_unique.values[0], df.values[0])
        tm.assert_numpy_array_equal(df_unique.values[1], df.values[1])