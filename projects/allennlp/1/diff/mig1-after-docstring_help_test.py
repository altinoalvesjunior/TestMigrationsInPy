#mig=assert

import argparse
import importlib
import io
import pkgutil
import re

import allennlp
from allennlp.commands import create_parser
from allennlp.common.testing import AllenNlpTestCase



class TestDocstringHelp(AllenNlpTestCase):
    RE_DOCSTRING_CALL_SUBCOMMAND_HELP = re.compile(r"^\s*\$ (allennlp (\S+) --help)$", re.MULTILINE)
    RE_STARTS_WITH_INDENTATION = re.compile(r"^ {4}", re.MULTILINE)

    def test_docstring_help(self):
        parent_module = allennlp.commands
        for module_info in pkgutil.iter_modules(
            parent_module.__path__, parent_module.__name__ + "."
        ):
            module = importlib.import_module(module_info.name)
            match = self.RE_DOCSTRING_CALL_SUBCOMMAND_HELP.search(module.__doc__)
            if match:
                expected_output = self.RE_STARTS_WITH_INDENTATION.sub(
                    "", module.__doc__[match.end(0) + 1 :]
                )

                str_call_subcommand_help = match.group(1)
                subcommand = match.group(2)
                actual_output = _subcommand_help_output(subcommand)

                assert expected_output == actual_output, (
                    f"The documentation for the subcommand usage"
                    f" in the module {module_info.name}"
                    f" does not match the output of running"
                    f" `{str_call_subcommand_help}`."
                    f" Please update the docstring to match the"
                    f" output."
                )
            else:
                assert module_info.name in [parent_module.__name__ + ".subcommand"], (
                    f"The documentation for the subcommand usage was not found within the docstring of"
                    f" the module {module_info.name}",
                )
