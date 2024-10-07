from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest

from ansible.module_utils.network.common.utils import to_list, sort_list
from ansible.module_utils.network.common.utils import dict_diff, dict_merge
from ansible.module_utils.network.common.utils import conditional, Template


class TestModuleUtilsNetworkCommon(unittest.TestCase):
    def test_dict_diff(self):
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
        self.assertNotIn('one', result)
        self.assertNotIn('two', result)
        self.assertEqual(result['three'], 4)
        self.assertEqual(result['four'], 4)
        # dict assertions
        self.assertIn('obj1', result)
        self.assertIn('key1', result['obj1'])
        self.assertNotIn('key2', result['obj1'])
        # list assertions
        self.assertEqual(result['l1'], [2, 1])
        self.assertNotIn('l2', result)
        self.assertEqual(result['l3'], [1])
        self.assertNotIn('l4', result)
        # nested assertions
        self.assertIn('obj1', result)
        self.assertEqual(result['obj1']['key1'], 2)
        self.assertNotIn('key2', result['obj1'])
        # bool assertions
        self.assertNotIn('b1', result)
        self.assertNotIn('b2', result)
        self.assertTrue(result['b3'])
        self.assertTrue(result['b4'])