from __future__ import unicode_literals
import os
import subprocess
import pytest
from cookiecutter import config, utils
from tests.skipif_markers import skipif_travis, skipif_no_network

@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are creating during the tests.
    """
    def fin_remove_additional_dirs():
        with utils.work_in(config.DEFAULT_CONFIG['cookiecutters_dir']):
            if os.path.isdir('cookiecutter-pypackage'):
                utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
    request.addfinalizer(fin_remove_additional_dirs)
    
@skipif_travis
@skipif_no_network
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_pypackage_git():
    proc = subprocess.Popen(
        'cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git',
        stdin=subprocess.PIPE,
        shell=True
    )
    # Just skip all the prompts
    proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')
    assert os.path.isfile('boilerplate/README.rst')