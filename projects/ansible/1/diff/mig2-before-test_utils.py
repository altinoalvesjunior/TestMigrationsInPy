from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest

from ansible.module_utils.network.common.utils import to_list, sort_list

class TestModuleUtilsNetworkCommon(unittest.TestCase):
    def test_sort(self):
        data = [3, 1, 2]
        self.assertEqual([1, 2, 3], sort_list(data))
        string_data = '123'
        self.assertEqual(string_data, sort_list(string_data))