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

class TestGenerateContext(CookiecutterCleanSystemTestCase):

    def test_generate_context_with_default(self):
        context = generate.generate_context(
            context_file='tests/test-generate-context/test.json',
            default_context={"1": 3}
        )
        self.assertEqual(context, {"test": {"1": 3, "some_key": "some_val"}})