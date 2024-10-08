import locale
import logging
import os
import pytest
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

def test_unknown_repo_type():
    repo_url = "http://norepotypespecified.com"
    with pytest.raises(exceptions.UnknownRepoType):
        vcs.identify_repo(repo_url)