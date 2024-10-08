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
    def test_run_shell_hooks(self):
        make_test_repo('tests/test-shellhooks')
        generate.generate_files(
            context={
                'cookiecutter': {'shellhooks': 'shellhooks'}
            },
            repo_dir='tests/test-shellhooks/',
            output_dir='tests/test-shellhooks/'
        )
        self.assertTrue(os.path.exists('tests/test-shellhooks/inputshellhooks/shell_pre.txt'))
        self.assertTrue(os.path.exists('tests/test-shellhooks/inputshellhooks/shell_post.txt'))