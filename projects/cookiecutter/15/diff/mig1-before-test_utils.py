import os
import sys
import stat
import unittest

from cookiecutter import utils

class TestUtils(unittest.TestCase):

    def test_workin(self):
        cwd = os.getcwd()
        ch_to = 'tests/files'

        class TestException(Exception):
            pass

        def test_work_in():
            with utils.work_in(ch_to):
                test_dir = os.path.join(cwd, ch_to).replace("/", os.sep)
                self.assertEqual(test_dir, os.getcwd())
                raise TestException()

        # Make sure we return to the correct folder
        self.assertEqual(cwd, os.getcwd())

        # Make sure that exceptions are still bubbled up
        self.assertRaises(TestException, test_work_in)