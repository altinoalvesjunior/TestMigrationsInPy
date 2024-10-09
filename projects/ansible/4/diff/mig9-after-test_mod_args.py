__metaclass__ = type

import pytest
from ansible.errors import AnsibleParserError
from ansible.parsing.mod_args import ModuleArgsParser


class TestModArgsDwim:
    @pytest.mark.parametrize("args_dict, msg", INVALID_MULTIPLE_ACTIONS)
    def test_multiple_actions(self, args_dict, msg):
        m = ModuleArgsParser(args_dict)
        with pytest.raises(AnsibleParserError) as err:
            m.parse()
        assert err.value.args[0] == msg
    def test_multiple_actions(self):
        args_dict = {'ping': 'data=hi', 'shell': 'echo hi'}
        m = ModuleArgsParser(args_dict)
        with pytest.raises(AnsibleParserError) as err:
            m.parse()

        assert err.value.args[0].startswith("conflicting action statements: ")
        conflicts = set(err.value.args[0][len("conflicting action statements: "):].split(', '))
        assert conflicts == set(('ping', 'shell'))