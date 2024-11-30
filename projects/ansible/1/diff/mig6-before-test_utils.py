from __future__ import (absolute_import, division)
__metaclass__ = type

from ansible.compat.tests import unittest

from ansible.module_utils.network.common.utils import conditional, Template


class TestModuleUtilsNetworkCommon(unittest.TestCase):
    def test_template(self):
        tmpl = Template()
        self.assertEqual('foo', tmpl('{{ test }}', {'test': 'foo'}))