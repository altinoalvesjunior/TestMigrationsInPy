import os
import pytest

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are created during the tests.
    """
    def fin_remove_additional_dirs():
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-input-extra'):
            utils.rmtree('fake-project-input-extra')
    request.addfinalizer(fin_remove_additional_dirs)
    
@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_input_extra_context(monkeypatch):
    """
    `Call cookiecutter()` with `no_input=False` and `extra_context`
    """
    monkeypatch.setattr(
        'cookiecutter.prompt.read_response',
        lambda x=u'': u'\n'
    )
    main.cookiecutter(
        'tests/fake-repo-pre',
        no_input=True,
        extra_context={'repo_name': 'fake-project-input-extra'}
    )
    assert os.path.isdir('fake-project-input-extra')