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
    def test_internal_keys(self):
        cb = CallbackBase()
        result = {'item': 'some_item',
                  '_ansible_some_var': 'SENTINEL',
                  'testing_ansible_out': 'should_be_left_in LEFTIN',
                  'invocation': 'foo --bar whatever [some_json]',
                  'some_dict_key': {'a_sub_dict_for_key': 'baz'},
                  'bad_dict_key': {'_ansible_internal_blah': 'SENTINEL'},
                  'changed': True}
        json_out = cb._dump_results(result)
        assert '"_ansible_' not in json_out
        assert 'SENTINEL' not in json_out
        assert 'LEFTIN' in json_out