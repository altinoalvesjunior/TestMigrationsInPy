from __future__ import unicode_literals
import logging
import os
import io
import sys
import stat
import unittest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter import exceptions
from cookiecutter import utils
from tests import CookiecutterCleanSystemTestCase

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class TestHooks(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        if os.path.exists('tests/test-pyhooks/inputpyhooks'):
            utils.rmtree('tests/test-pyhooks/inputpyhooks')
        if os.path.exists('inputpyhooks'):
            utils.rmtree('inputpyhooks')
        if os.path.exists('tests/test-shellhooks'):
            utils.rmtree('tests/test-shellhooks')
        super(TestHooks, self).tearDown()

    def test_ignore_hooks_dirs(self):
        generate.generate_files(
            context={
                'cookiecutter': {'pyhooks': 'pyhooks'}
            },
            repo_dir='tests/test-pyhooks/',
            output_dir='tests/test-pyhooks/'
        )
        self.assertFalse(os.path.exists('tests/test-pyhooks/inputpyhooks/hooks'))