import shutil
import pytest

from cookiecutter import config

@pytest.fixture(scope='module')
def user_config_path():
    return os.path.expanduser('~/.cookiecutterrc')

def test_get_user_config_valid(user_config_path):
    """ Get config from a valid ~/.cookiecutterrc file """
    shutil.copy('tests/test-config/valid-config.yaml', user_config_path)
    conf = config.get_user_config()
    expected_conf = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'default_context': {
            "full_name": "Firstname Lastname",
            "email": "firstname.lastname@gmail.com",
            "github_username": "example"
        }
    }
    assert conf == expected_conf