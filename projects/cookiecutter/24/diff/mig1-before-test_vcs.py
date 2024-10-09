import locale
import logging
import os
import subprocess
import unittest

from cookiecutter.compat import patch
from cookiecutter import exceptions, utils, vcs

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
encoding = locale.getdefaultlocale()[1]


class TestIdentifyRepo(unittest.TestCase):
    def test_identify_git_github(self):
        repo_url = "https://github.com/audreyr/cookiecutter-pypackage.git"
        self.assertEqual(vcs.identify_repo(repo_url), "git")