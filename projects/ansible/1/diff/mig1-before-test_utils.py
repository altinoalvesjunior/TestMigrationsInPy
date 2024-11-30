from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest

from ansible.module_utils.network.common.utils import to_list, sort_list


class TestModuleUtilsNetworkCommon(unittest.TestCase):
    def test_to_list(self):
        for scalar in ('string', 1, True, False, None):
            self.assertTrue(isinstance(to_list(scalar), list))
        for container in ([1, 2, 3], {'one': 1}):
            self.assertTrue(isinstance(to_list(container), list))
        test_list = [1, 2, 3]
        self.assertNotEqual(id(test_list), id(to_list(test_list)))