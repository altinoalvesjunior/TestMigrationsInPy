__metaclass__ = type

import pytest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim:
    def test_local_action_string(self):
        m = ModuleArgsParser(dict(local_action='copy src=a dest=b'))
        mod, args, delegate_to = m.parse()
        self._debug(mod, args, delegate_to)

        assert mod == 'copy'
        assert args == dict(src='a', dest='b')
        assert delegate_to == 'localhost'