from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim(unittest.TestCase):
    def test_shell_with_modifiers(self):
        m = ModuleArgsParser(dict(shell='/bin/foo creates=/tmp/baz removes=/tmp/bleep'))
        mod, args, to = m.parse()
        self._debug(mod, args, to)
        self.assertEqual(mod, 'command')
        self.assertEqual(args, dict(
            creates='/tmp/baz',
            removes='/tmp/bleep',
            _raw_params='/bin/foo',
            _uses_shell=True,
        ))
        self.assertIsNone(to)