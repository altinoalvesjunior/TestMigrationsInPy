import pytest
from datetime import datetime, timedelta, date
import numpy as np

from pandas import Timedelta, Timestamp, DatetimeIndex
from pandas.types.cast import (maybe_downcast_to_dtype,
                               maybe_convert_objects,
                               infer_dtype_from_scalar,
                               infer_dtype_from_array,
                               maybe_convert_string_to_object,
                               maybe_convert_scalar,
                               find_common_type)
from pandas.types.dtypes import (CategoricalDtype,
                                 DatetimeTZDtype, PeriodDtype)
from pandas.util import testing as tm

class TestInferDtype(object):
    def test_infer_dtype_from_scalar(self):
        # Test that _infer_dtype_from_scalar is returning correct dtype for int
        # and float.

        for dtypec in [np.uint8, np.int8, np.uint16, np.int16, np.uint32,
                       np.int32, np.uint64, np.int64]:
            data = dtypec(12)
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == type(data)

        data = 12
        dtype, val = infer_dtype_from_scalar(data)
        assert dtype == np.int64

        for dtypec in [np.float16, np.float32, np.float64]:
            data = dtypec(12)
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == dtypec

        data = np.float(12)
        dtype, val = infer_dtype_from_scalar(data)
        assert dtype == np.float64

        for data in [True, False]:
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == np.bool_

        for data in [np.complex64(1), np.complex128(1)]:
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == np.complex_

        for data in [np.datetime64(1, 'ns'), Timestamp(1),
                     datetime(2000, 1, 1, 0, 0)]:
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == 'M8[ns]'

        for data in [np.timedelta64(1, 'ns'), Timedelta(1),
                     timedelta(1)]:
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == 'm8[ns]'

        for data in [date(2000, 1, 1),
                     Timestamp(1, tz='US/Eastern'), 'foo']:
            dtype, val = infer_dtype_from_scalar(data)
            assert dtype == np.object_