from __future__ import unicode_literals
import os
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
def test_run_python_hooks_cwd():
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir='tests/test-pyhooks/'
    )
    assert os.path.exists('inputpyhooks/python_pre.txt')
    assert os.path.exists('inputpyhooks/python_post.txt')