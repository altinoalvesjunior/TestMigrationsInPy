from collections import OrderedDict
import inspect
import json
import os
import shutil
import unittest
import plotly
from dash.development.base_component import Component
from dash.development.component_generator import reserved_words
from dash.development._py_components_generation import (
    generate_class_string,
    generate_class_file,
    generate_class,
    create_docstring,
    prohibit_events,
    js_to_py_type
)

_dir = os.path.dirname(os.path.abspath(__file__))

Component._prop_names = ('id', 'a', 'children', 'style', )
Component._type = 'TestComponent'
Component._namespace = 'test_namespace'
Component._valid_wildcard_attributes = ['data-', 'aria-']

class TestGenerateClassFile(unittest.TestCase):
    def setUp(self):
        json_path = os.path.join(_dir, 'metadata_test.json')
        with open(json_path) as data_file:
            json_string = data_file.read()
            data = json\
                .JSONDecoder(object_pairs_hook=OrderedDict)\
                .decode(json_string)
            self.data = data

        # Create a folder for the new component file
        os.makedirs('TableComponents')

        # Import string not included in generated class string
        import_string =\
            "# AUTO GENERATED FILE - DO NOT EDIT\n\n" + \
            "from dash.development.base_component import" + \
            " Component, _explicitize_args\n\n\n"

        # Class string generated from generate_class_string
        self.component_class_string = import_string + generate_class_string(
            typename='Table',
            props=data['props'],
            description=data['description'],
            namespace='TableComponents'
        )

        # Class string written to file
        generate_class_file(
            typename='Table',
            props=data['props'],
            description=data['description'],
            namespace='TableComponents'
        )
        written_file_path = os.path.join(
            'TableComponents', "Table.py"
        )
        with open(written_file_path, 'r') as f:
            self.written_class_string = f.read()

        # The expected result for both class string and class file generation
        expected_string_path = os.path.join(_dir, 'metadata_test.py')
        with open(expected_string_path, 'r') as f:
            self.expected_class_string = f.read()

    def tearDown(self):
        shutil.rmtree('TableComponents')