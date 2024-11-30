from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest

from ansible.module_utils.network.common.utils import conditional, Template


class TestModuleUtilsNetworkCommon(unittest.TestCase):
    def test_conditional(self):
        self.assertTrue(conditional(10, 10))
        self.assertTrue(conditional('10', '10'))
        self.assertTrue(conditional('foo', 'foo'))
        self.assertTrue(conditional(True, True))
        self.assertTrue(conditional(False, False))
        self.assertTrue(conditional(None, None))
        self.assertTrue(conditional("ge(1)", 1))
        self.assertTrue(conditional("gt(1)", 2))
        self.assertTrue(conditional("le(2)", 2))
        self.assertTrue(conditional("lt(3)", 2))
        self.assertTrue(conditional("eq(1)", 1))
        self.assertTrue(conditional("neq(0)", 1))
        self.assertTrue(conditional("min(1)", 1))
        self.assertTrue(conditional("max(1)", 1))
        self.assertTrue(conditional("exactly(1)", 1))