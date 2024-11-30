from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest

from ansible.module_utils.network.common.utils import dict_diff, dict_merge


class TestModuleUtilsNetworkCommon(unittest.TestCase):
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
        self.assertIn('one', result)
        self.assertIn('two', result)
        self.assertEqual(result['three'], 4)
        self.assertEqual(result['four'], 4)
        # dict assertions
        self.assertIn('obj1', result)
        self.assertIn('key1', result['obj1'])
        self.assertIn('key2', result['obj1'])
        # list assertions
        self.assertEqual(result['l1'], [1, 2, 3])
        self.assertIn('l2', result)
        self.assertEqual(result['l3'], [1])
        self.assertIn('l4', result)
        # nested assertions
        self.assertIn('obj1', result)
        self.assertEqual(result['obj1']['key1'], 2)
        self.assertIn('key2', result['obj1'])
        # bool assertions
        self.assertIn('b1', result)
        self.assertIn('b2', result)
        self.assertTrue(result['b3'])
        self.assertTrue(result['b4'])