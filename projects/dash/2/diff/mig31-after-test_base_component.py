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

class TestGenerateClass:
    @pytest.fixture(autouse=True)
    def setup_function(self):
        path = os.path.join(_dir, 'metadata_test.json')
        with open(path) as data_file:
            json_string = data_file.read()
            data = json\
                .JSONDecoder(object_pairs_hook=OrderedDict)\
                .decode(json_string)
            self.data = data

        self.ComponentClass = generate_class(
            typename='Table',
            props=data['props'],
            description=data['description'],
            namespace='TableComponents'
        )

        path = os.path.join(_dir, 'metadata_required_test.json')
        with open(path) as data_file:
            json_string = data_file.read()
            required_data = json\
                .JSONDecoder(object_pairs_hook=OrderedDict)\
                .decode(json_string)
            self.required_data = required_data

        self.ComponentClassRequired = generate_class(
            typename='TableRequired',
            props=required_data['props'],
            description=required_data['description'],
            namespace='TableComponents'
        )
        
        def test_repr_multiple_arguments(self):
        # Note how the order in which keyword arguments are supplied is
        # not always equal to the order in the repr of the component
            c = self.ComponentClass(id='my id', optionalArray=[1, 2, 3])
            assert repr(c) == "Table(optionalArray=[1, 2, 3], id='my id')"
        
        