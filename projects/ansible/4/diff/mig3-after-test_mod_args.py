__metaclass__ = type

import pytest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim:
    def test_shell_with_modifiers(self):
        m = ModuleArgsParser(dict(shell='/bin/foo creates=/tmp/baz removes=/tmp/bleep'))
        mod, args, to = m.parse()
        self._debug(mod, args, to)
        assert mod == 'shell'
        assert args == dict(
            creates='/tmp/baz',
            removes='/tmp/bleep',
            _raw_params='/bin/foo',
        )
        assert to is None