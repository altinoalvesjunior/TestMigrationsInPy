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
    def test_is_mixed_dtype(self):
        assert not create_mgr('a,b:f8').is_mixed_type
        assert not create_mgr('a:f8-1; b:f8-2').is_mixed_type

        assert create_mgr('a,b:f8; c,d: f4').is_mixed_type
        assert create_mgr('a,b:f8; c,d: object').is_mixed_type