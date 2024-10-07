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

class TestGenerateFiles(CookiecutterCleanSystemTestCase):
    def tearDown(self):
        if os.path.exists('inputpizzä'):
            utils.rmtree('inputpizzä')
        if os.path.exists('inputgreen'):
            utils.rmtree('inputgreen')
        if os.path.exists('inputbinary_files'):
            utils.rmtree('inputbinary_files')
        if os.path.exists('tests/custom_output_dir'):
            utils.rmtree('tests/custom_output_dir')
        if os.path.exists('inputpermissions'):
            utils.rmtree('inputpermissions')
        super(TestGenerateFiles, self).tearDown()
    def test_generate_files_permissions(self):
        """
        simple.txt and script.sh should retain their respective 0o644 and
        0o755 permissions
        """
        generate.generate_files(
            context={
                'cookiecutter': {'permissions': 'permissions'}
            },
            repo_dir='tests/test-generate-files-permissions'
        )
        self.assertTrue(os.path.isfile('inputpermissions/simple.txt'))
        # simple.txt should still be 0o644
        self.assertEquals(
            os.stat('tests/test-generate-files-permissions/input{{cookiecutter.permissions}}/simple.txt').st_mode & 0o777,
            os.stat('inputpermissions/simple.txt').st_mode & 0o777
        )
        self.assertTrue(os.path.isfile('inputpermissions/script.sh'))
        # script.sh should still be 0o755
        self.assertEquals(
            os.stat('tests/test-generate-files-permissions/input{{cookiecutter.permissions}}/script.sh').st_mode & 0o777,
            os.stat('inputpermissions/script.sh').st_mode & 0o777
        )