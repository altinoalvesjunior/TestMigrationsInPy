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

class TestCaseDictMerge:
    def test_dict_merge(self):
        base = dict(obj2=dict(), b1=True, b2=False, b3=False,
                    one=1, two=2, three=3, obj1=dict(key1=1, key2=2),
                    l1=[1, 3], l2=[1, 2, 3], l4=[4],
                    nested=dict(n1=dict(n2=2)))

        other = dict(b1=True, b2=False, b3=True, b4=True,
                     one=1, three=4, four=4, obj1=dict(key1=2),
                     l1=[2, 1], l2=[3, 2, 1], l3=[1],
                     nested=dict(n1=dict(n2=2, n3=3)))

        result = dict_merge(base, other)
        
        # string assertions
        assert 'one' in result
        assert 'two' in result
        assert result['three'] == 4
        assert result['four'] == 4

        # dict assertions
        assert 'obj1' in result
        assert 'key1' in result['obj1']
        assert 'key2' in result['obj1']

        # list assertions
        # this line differs from the network_utils/common test of the function of the
        # same name as this method does not merge lists
        assert result['l1'], [2, 1]
        assert 'l2' in result
        assert result['l3'], [1]
        assert 'l4' in result

        # nested assertions
        assert 'obj1' in result
        assert result['obj1']['key1'], 2
        assert 'key2' in result['obj1']

        # bool assertions
        assert 'b1' in result
        assert 'b2' in result
        assert result['b3']
        assert result['b4']