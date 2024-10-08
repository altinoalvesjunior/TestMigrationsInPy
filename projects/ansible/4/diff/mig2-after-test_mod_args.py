__metaclass__ = type

import pytest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim:
    def test_basic_command(self):
        m = ModuleArgsParser(dict(command='echo hi'))
        mod, args, to = m.parse()
        self._debug(mod, args, to)
        assert mod == 'command'
        assert args == dict(
            _raw_params='echo hi',
        )
        assert to is None