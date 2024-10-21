from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.tests import unittest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim(unittest.TestCase):
    def test_local_action_string(self):
        m = ModuleArgsParser(dict(local_action='copy src=a dest=b'))
        mod, args, delegate_to = m.parse()
        self._debug(mod, args, delegate_to)
        self.assertEqual(mod, 'copy')
        self.assertEqual(args, dict(src='a', dest='b'))
        self.assertIs(delegate_to, 'localhost')

   