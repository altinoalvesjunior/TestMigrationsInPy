from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.network.common.utils import to_list, sort_list


def test_to_list():
    for scalar in ('string', 1, True, False, None):
        assert isinstance(to_list(scalar), list)
    for container in ([1, 2, 3], {'one': 1}):
        assert isinstance(to_list(container), list)
    test_list = [1, 2, 3]
    assert id(test_list) != id(to_list(test_list))