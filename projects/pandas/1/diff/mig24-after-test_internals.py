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
    def test_convert(self):
        def _compare(old_mgr, new_mgr):
            """ compare the blocks, numeric compare ==, object don't """
            old_blocks = set(old_mgr.blocks)
            new_blocks = set(new_mgr.blocks)
            assert len(old_blocks) == len(new_blocks)

            # compare non-numeric
            for b in old_blocks:
                found = False
                for nb in new_blocks:
                    if (b.values == nb.values).all():
                        found = True
                        break
                assert found

            for b in new_blocks:
                found = False
                for ob in old_blocks:
                    if (b.values == ob.values).all():
                        found = True
                        break
                assert found

        # noops
        mgr = create_mgr('f: i8; g: f8')
        new_mgr = mgr.convert()
        _compare(mgr, new_mgr)

        mgr = create_mgr('a, b: object; f: i8; g: f8')
        new_mgr = mgr.convert()
        _compare(mgr, new_mgr)

        # convert
        mgr = create_mgr('a,b,foo: object; f: i8; g: f8')
        mgr.set('a', np.array(['1'] * N, dtype=np.object_))
        mgr.set('b', np.array(['2.'] * N, dtype=np.object_))
        mgr.set('foo', np.array(['foo.'] * N, dtype=np.object_))
        new_mgr = mgr.convert(numeric=True)
        assert new_mgr.get('a').dtype == np.int64
        assert new_mgr.get('b').dtype == np.float64
        assert new_mgr.get('foo').dtype == np.object_
        assert new_mgr.get('f').dtype == np.int64
        assert new_mgr.get('g').dtype == np.float64

        mgr = create_mgr('a,b,foo: object; f: i4; bool: bool; dt: datetime;'
                         'i: i8; g: f8; h: f2')
        mgr.set('a', np.array(['1'] * N, dtype=np.object_))
        mgr.set('b', np.array(['2.'] * N, dtype=np.object_))
        mgr.set('foo', np.array(['foo.'] * N, dtype=np.object_))
        new_mgr = mgr.convert(numeric=True)
        assert new_mgr.get('a').dtype == np.int64
        assert new_mgr.get('b').dtype == np.float64
        assert new_mgr.get('foo').dtype == np.object_
        assert new_mgr.get('f').dtype == np.int32
        assert new_mgr.get('bool').dtype == np.bool_
        assert new_mgr.get('dt').dtype.type, np.datetime64
        assert new_mgr.get('i').dtype == np.int64
        assert new_mgr.get('g').dtype == np.float64
        assert new_mgr.get('h').dtype == np.float16