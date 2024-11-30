from __future__ import absolute_import, division, print_function
__metaclass__ = type

import pytest

from ansible.module_utils.network.common.utils import dict_diff, dict_merge

def test_dict_diff():
    base = dict(obj2=dict(), b1=True, b2=False, b3=False,
                one=1, two=2, three=3, obj1=dict(key1=1, key2=2),
                l1=[1, 3], l2=[1, 2, 3], l4=[4],
                nested=dict(n1=dict(n2=2)))
    other = dict(b1=True, b2=False, b3=True, b4=True,
                 one=1, three=4, four=4, obj1=dict(key1=2),
                 l1=[2, 1], l2=[3, 2, 1], l3=[1],
                 nested=dict(n1=dict(n2=2, n3=3)))
    result = dict_diff(base, other)
    # string assertions
    assert 'one' not in result
    assert 'two' not in result
    assert result['three'] == 4
    assert result['four'] == 4
    # dict assertions
    assert 'obj1' in result
    assert 'key1' in result['obj1']
    assert 'key2' not in result['obj1']
    # list assertions
    assert result['l1'] == [2, 1]
    assert 'l2' not in result
    assert result['l3'] == [1]
    assert 'l4' not in result
    # nested assertions
    assert 'obj1' in result
    assert result['obj1']['key1'] == 2
    assert 'key2' not in result['obj1']
    # bool assertions
    assert 'b1' not in result
    assert 'b2' not in result
    assert result['b3']
    assert result['b4']