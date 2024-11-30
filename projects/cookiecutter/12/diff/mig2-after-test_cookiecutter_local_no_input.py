import os
import pytest

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are creating during the tests.
    """
    def fin_remove_additional_dirs():
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-extra'):
            utils.rmtree('fake-project-extra')
        if os.path.isdir('fake-project-templated'):
            utils.rmtree('fake-project-templated')
    request.addfinalizer(fin_remove_additional_dirs)
    
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_templated_context():
    """
    `Call cookiecutter()` with `no_input=True` and templates in the
    cookiecutter.json file
    """
    main.cookiecutter(
        'tests/fake-repo-tmpl',
        no_input=True
    )
    assert os.path.isdir('fake-project-templated')