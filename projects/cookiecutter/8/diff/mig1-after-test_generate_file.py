from __future__ import unicode_literals
import os
import pytest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_cheese_file(request):
    """
    Remove the cheese text file which is created by the tests.
    """
    def fin_remove_cheese_file():
        if os.path.exists('tests/files/cheese.txt'):
            os.remove('tests/files/cheese.txt')
    request.addfinalizer(fin_remove_cheese_file)
    
@pytest.mark.usefixtures('remove_cheese_file')
def test_generate_file_verbose_template_syntax_error():
    env = Environment()
    env.loader = FileSystemLoader('.')
    try:
        generate.generate_file(
            project_dir=".",
            infile='tests/files/syntax_error.txt',
            context={'syntax_error': 'syntax_error'},
            env=env
        )
    except TemplateSyntaxError as exception:
        expected = (
            'Missing end of comment tag\n'
            '  File "./tests/files/syntax_error.txt", line 1\n'
            '    I eat {{ syntax_error }} {# this comment is not closed}'
        )
        expected = expected.replace("/", os.sep)
        assert str(exception) == expected
    except Exception as exception:
        pytest.fail('Unexpected exception thrown: {0}'.format(exception))
    else:
        pytest.fail('TemplateSyntaxError not thrown')