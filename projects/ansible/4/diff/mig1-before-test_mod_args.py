from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim(unittest.TestCase):
    def test_basic_shell(self):
        m = ModuleArgsParser(dict(shell='echo hi'))
        mod, args, to = m.parse()
        self._debug(mod, args, to)
        self.assertEqual(mod, 'command')
        self.assertEqual(args, dict(
            _raw_params='echo hi',
            _uses_shell=True,
        ))
        self.assertIsNone(to)