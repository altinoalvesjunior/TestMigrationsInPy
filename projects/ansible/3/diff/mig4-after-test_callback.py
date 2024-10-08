from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import re
import textwrap
import types

from units.compat import unittest
from units.compat.mock import patch, mock_open, MagicMock

import pytest

from ansible.plugins.callback import CallbackBase

class TestCallbackDumpResults(object):
     def test_diff(self):
        cb = CallbackBase()
        result = {'item': 'some_item LEFTIN',
                  'diff': ['remove stuff', 'added LEFTIN'],
                  '_ansible_verbose_always': 'chicane'}
        json_out = cb._dump_results(result)
        assert 'SENTINEL' not in json_out
        assert 'LEFTIN' in json_out
