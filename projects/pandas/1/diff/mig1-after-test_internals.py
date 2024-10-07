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

@pytest.fixture
def mgr():
    return create_mgr(
        'a: f8; b: object; c: f8; d: object; e: f8;'
        'f: bool; g: i8; h: complex; i: datetime-1; j: datetime-2;'
        'k: M8[ns, US/Eastern]; l: M8[ns, CET];')
