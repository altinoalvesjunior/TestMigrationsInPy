import logging
import os

from cookiecutter.compat import patch, unittest
from cookiecutter import main, utils
from tests import CookiecutterCleanSystemTestCase

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False

# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class TestCookiecutterLocalWithInput(CookiecutterCleanSystemTestCase):
    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_cookiecutter_input_extra_context(self):
        """ `Call cookiecutter()` with `no_input=False` and `extra_context` """
        main.cookiecutter(
            'tests/fake-repo-pre',
            no_input=True,
            extra_context={'repo_name': 'fake-project-input-extra'}
        )
        self.assertTrue(os.path.isdir('fake-project-input-extra'))
    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-input-extra'):
            utils.rmtree('fake-project-input-extra')
