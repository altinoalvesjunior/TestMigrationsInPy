from __future__ import unicode_literals
import os
import subprocess
import pytest
from cookiecutter import utils
from tests.skipif_markers import skipif_travis, skipif_no_network

@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are creating during the tests.
    """
    def fin_remove_additional_dirs():
        if os.path.isdir('cookiecutter-jquery'):
            utils.rmtree('cookiecutter-jquery')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
    request.addfinalizer(fin_remove_additional_dirs)