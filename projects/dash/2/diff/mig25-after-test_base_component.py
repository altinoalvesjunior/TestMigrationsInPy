import inspect
import json
import os
import shutil
from collections import OrderedDict
import plotly
import pytest
from dash.development._py_components_generation import (
    generate_class_string,
    generate_class_file,
    generate_class,
    create_docstring,
    prohibit_events,
    js_to_py_type
)
from dash.development.base_component import Component
from dash.development.component_generator import reserved_words

_dir = os.path.dirname(os.path.abspath(__file__))

Component._prop_names = ('id', 'a', 'children', 'style', )
Component._type = 'TestComponent'
Component._namespace = 'test_namespace'
Component._valid_wildcard_attributes = ['data-', 'aria-']

class TestGenerateClassFile:
     def assert_no_trailing_spaces(self, s):
        for line in s.split('\n'):
            assert line == line.rstrip()