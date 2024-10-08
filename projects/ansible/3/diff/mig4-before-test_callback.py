from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
import textwrap
import types

from units.compat import unittest
from units.compat.mock import patch, mock_open, MagicMock


from ansible.plugins.callback import CallbackBase

class TestCallbackDumpResults(unittest.TestCase):
    def test_diff(self):
        cb = CallbackBase()
        result = {'item': 'some_item LEFTIN',
                  'diff': ['remove stuff', 'added LEFTIN'],
                  '_ansible_verbose_always': 'chicane'}
        json_out = cb._dump_results(result)
        self.assertFalse('SENTINEL' in json_out)
        self.assertTrue('LEFTIN' in json_out)