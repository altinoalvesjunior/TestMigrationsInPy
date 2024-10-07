from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.network.common.utils import to_list, sort_list
from ansible.module_utils.network.common.utils import dict_diff, dict_merge
from ansible.module_utils.network.common.utils import conditional, Template
from ansible.module_utils.network.common.utils import to_masklen, to_netmask, to_subnet, to_ipv6_network
from ansible.module_utils.network.common.utils import is_masklen, is_netmask

def test_conditional():
    assert conditional(10, 10)
    assert conditional('10', '10')
    assert conditional('foo', 'foo')
    assert conditional(True, True)
    assert conditional(False, False)
    assert conditional(None, None)
    assert conditional("ge(1)", 1)
    assert conditional("gt(1)", 2)
    assert conditional("le(2)", 2)
    assert conditional("lt(3)", 2)
    assert conditional("eq(1)", 1)
    assert conditional("neq(0)", 1)
    assert conditional("min(1)", 1)
    assert conditional("max(1)", 1)
    assert conditional("exactly(1)", 1)