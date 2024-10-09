__metaclass__ = type

import pytest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim:
    def test_normal_usage(self):
        m = ModuleArgsParser(dict(copy='src=a dest=b'))
        mod, args, to = m.parse()
        self._debug(mod, args, to)
        assert mod, 'copy'
        assert args, dict(src='a', dest='b')
        assert to is None