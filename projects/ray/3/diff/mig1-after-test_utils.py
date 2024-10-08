import time
import pytest

from ray.tune.search.variant_generator import format_vars
from ray.tune.utils.util import retry_fn

def test_format_vars():

    # Format brackets correctly
    assert (
        format_vars(
            {
                ("a", "b", "c"): 8.1234567,
                ("a", "b", "d"): [7, 8],
                ("a", "b", "e"): [[[3, 4]]],
            }
        )
        == "c=8.1235,d=7_8,e=3_4"
    )
    # Sorted by full keys, but only last key is reported
    assert (
        format_vars(
            {
                ("a", "c", "x"): [7, 8],
                ("a", "b", "x"): 8.1234567,
            }
        )
        == "x=8.1235,x=7_8"
    )
    # Filter out invalid chars. It's ok to have empty keys or values.
    assert (
        format_vars(
            {
                ("a  c?x",): " <;%$ok ",
                ("some",): " ",
            }
        )
        == "a_c_x=ok,some="
    )