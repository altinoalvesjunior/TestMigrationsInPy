from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible.module_utils.common.dict_transformations import (
    _camel_to_snake,
    _snake_to_camel,
    camel_dict_to_snake_dict,
    dict_merge,
    recursive_diff,
)

EXPECTED_SNAKIFICATION = {
    'alllower': 'alllower',
    'TwoWords': 'two_words',
    'AllUpperAtEND': 'all_upper_at_end',
    'AllUpperButPLURALs': 'all_upper_but_plurals',
    'TargetGroupARNs': 'target_group_arns',
    'HTTPEndpoints': 'http_endpoints',
    'PLURALs': 'plurals'
}

EXPECTED_REVERSIBLE = {
    'TwoWords': 'two_words',
    'AllUpperAtEND': 'all_upper_at_e_n_d',
    'AllUpperButPLURALs': 'all_upper_but_p_l_u_r_a_ls',
    'TargetGroupARNs': 'target_group_a_r_ns',
    'HTTPEndpoints': 'h_t_t_p_endpoints',
    'PLURALs': 'p_l_u_r_a_ls'
}

class TestCaseCamelToSnakeAndBack:
    def test_camel_to_snake_and_back(self):
        for (k, v) in EXPECTED_REVERSIBLE.items():
            assert _snake_to_camel(_camel_to_snake(k, reversible=True), capitalize_first=True) == k