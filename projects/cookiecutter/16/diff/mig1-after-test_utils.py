import os
import sys
import stat
import unittest
import pytest

from cookiecutter import utils

def test_workin():
    cwd = os.getcwd()
    ch_to = 'tests/files'

    class TestException(Exception):
        pass

    def test_work_in():
        with utils.work_in(ch_to):
            test_dir = os.path.join(cwd, ch_to).replace("/", os.sep)
            assert test_dir == os.getcwd()
            raise TestException()

    # Make sure we return to the correct folder
    assert cwd == os.getcwd()

    # Make sure that exceptions are still bubbled up
    with pytest.raises(TestException):
        test_work_in()