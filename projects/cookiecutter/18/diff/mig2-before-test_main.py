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


class TestCookiecutterLocalNoInput(CookiecutterCleanSystemTestCase):
    def test_cookiecutter_templated_context(self):
        """
        `Call cookiecutter()` with `no_input=True` and templates in the
        cookiecutter.json file
        """
        main.cookiecutter(
            'tests/fake-repo-tmpl',
            no_input=True
        )
        self.assertTrue(os.path.isdir('fake-project-templated'))
    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-extra'):
            utils.rmtree('fake-project-extra')
        if os.path.isdir('fake-project-templated'):
            utils.rmtree('fake-project-templated')