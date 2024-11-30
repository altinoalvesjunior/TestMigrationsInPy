from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.network.common.utils import to_list, sort_list

def test_sort():
    data = [3, 1, 2]
    assert [1, 2, 3] == sort_list(data)
    string_data = '123'
    assert string_data == sort_list(string_data)