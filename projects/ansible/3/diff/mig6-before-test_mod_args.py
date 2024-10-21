from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim(unittest.TestCase):
    def test_action_with_complex(self):
        m = ModuleArgsParser(dict(action=dict(module='copy', src='a', dest='b')))
        mod, args, to = m.parse()
        self._debug(mod, args, to)
        self.assertEqual(mod, 'copy')
        self.assertEqual(args, dict(src='a', dest='b'))
        self.assertIsNone(to)