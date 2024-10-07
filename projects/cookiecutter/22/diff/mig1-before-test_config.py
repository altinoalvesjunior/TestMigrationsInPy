import os
import shutil

from cookiecutter.compat import unittest
from cookiecutter import config
from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration


class TestGetUserConfig(unittest.TestCase):
    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
    )
        
    def test_get_user_config_valid(self):
        """ Get config from a valid ~/.cookiecutterrc file """
        shutil.copy('tests/test-config/valid-config.yaml', self.user_config_path)
        conf = config.get_user_config()
        expected_conf = {
        	'cookiecutters_dir': '/home/example/some-path-to-templates',
        	'default_context': {
        		"full_name": "Firstname Lastname",
        		"email": "firstname.lastname@gmail.com",
        		"github_username": "example"
        	}
        }
        self.assertEqual(conf, expected_conf)