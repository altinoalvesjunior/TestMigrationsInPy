from __future__ import unicode_literals
import os
import sys
import stat
import pytest

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_additional_folders(request):
    """
    Remove some special folders which are created by the tests.
    """
    def fin_remove_additional_folders():
        if os.path.exists('tests/test-pyhooks/inputpyhooks'):
            utils.rmtree('tests/test-pyhooks/inputpyhooks')
        if os.path.exists('inputpyhooks'):
            utils.rmtree('inputpyhooks')
        if os.path.exists('tests/test-shellhooks'):
            utils.rmtree('tests/test-shellhooks')
    request.addfinalizer(fin_remove_additional_folders)

@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_shell_hooks():
    make_test_repo('tests/test-shellhooks')
    generate.generate_files(
        context={
            'cookiecutter': {'shellhooks': 'shellhooks'}
        },
        repo_dir='tests/test-shellhooks/',
        output_dir='tests/test-shellhooks/'
    )
    shell_pre_file = 'tests/test-shellhooks/inputshellhooks/shell_pre.txt'
    shell_post_file = 'tests/test-shellhooks/inputshellhooks/shell_post.txt'
    assert os.path.exists(shell_pre_file)
    assert os.path.exists(shell_post_file)