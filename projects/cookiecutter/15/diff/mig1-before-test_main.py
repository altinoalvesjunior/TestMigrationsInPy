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

class TestAbbreviationExpansion(unittest.TestCase):

    def test_abbreviation_expansion(self):
        input_dir = main.expand_abbreviations('foo', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(input_dir, 'bar')