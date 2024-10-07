from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.network.common.utils import to_list, sort_list
from ansible.module_utils.network.common.utils import dict_diff, dict_merge
from ansible.module_utils.network.common.utils import conditional, Template
from ansible.module_utils.network.common.utils import to_masklen, to_netmask, to_subnet, to_ipv6_network
from ansible.module_utils.network.common.utils import is_masklen, is_netmask

def test_sort():
    data = [3, 1, 2]
    assert [1, 2, 3] == sort_list(data)
    string_data = '123'
    assert string_data == sort_list(string_data)