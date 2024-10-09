from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim(unittest.TestCase):
    def test_multiple_actions(self):
        m = ModuleArgsParser(dict(action='shell echo hi', local_action='shell echo hi'))
        self.assertRaises(AnsibleParserError, m.parse)

        m = ModuleArgsParser(dict(action='shell echo hi', shell='echo hi'))
        self.assertRaises(AnsibleParserError, m.parse)

        m = ModuleArgsParser(dict(local_action='shell echo hi', shell='echo hi'))
        self.assertRaises(AnsibleParserError, m.parse)

        m = ModuleArgsParser(dict(ping='data=hi', shell='echo hi'))
        self.assertRaises(AnsibleParserError, m.parse)