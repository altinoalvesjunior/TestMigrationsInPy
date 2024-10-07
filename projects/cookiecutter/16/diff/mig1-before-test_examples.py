from __future__ import unicode_literals
import logging
import os
import subprocess
from cookiecutter.compat import unittest
from cookiecutter import config, utils
from tests import CookiecutterCleanSystemTestCase
try:
    travis = os.environ[u'TRAVIS']
except KeyError:
    travis = False
try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False
    
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub.')
class TestExamplesRepoArg(CookiecutterCleanSystemTestCase):
    def tearDown(self):
        with utils.work_in(config.DEFAULT_CONFIG['cookiecutters_dir']):
            if os.path.isdir('cookiecutter-pypackage'):
                utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
        super(TestExamplesRepoArg, self).tearDown()