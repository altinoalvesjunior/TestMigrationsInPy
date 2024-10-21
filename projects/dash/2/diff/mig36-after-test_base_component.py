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

class TestMetaDataConversions:
    @pytest.fixture(autouse=True)
    def setup_function(self):
        path = os.path.join(_dir, 'metadata_test.json')
        with open(path) as data_file:
            json_string = data_file.read()
            data = json\
                .JSONDecoder(object_pairs_hook=OrderedDict)\
                .decode(json_string)
            self.data = data

        self.expected_arg_strings = OrderedDict([
            ['children',
             'a list of or a singular dash component, string or number'],

            ['optionalArray', 'list'],

            ['optionalBool', 'boolean'],

            ['optionalFunc', ''],

            ['optionalNumber', 'number'],

            ['optionalObject', 'dict'],

            ['optionalString', 'string'],

            ['optionalSymbol', ''],

            ['optionalElement', 'dash component'],

            ['optionalNode',
             'a list of or a singular dash component, string or number'],

            ['optionalMessage', ''],

            ['optionalEnum', 'a value equal to: \'News\', \'Photos\''],

            ['optionalUnion', 'string | number'],

            ['optionalArrayOf', 'list of numbers'],

            ['optionalObjectOf',
             'dict with strings as keys and values of type number'],

            ['optionalObjectWithExactAndNestedDescription', '\n'.join([

                "dict containing keys 'color', 'fontSize', 'figure'.",
                "Those keys have the following types:",
                "  - color (string; optional)",
                "  - fontSize (number; optional)",
                "  - figure (optional): Figure is a plotly graph object. figure has the following type: dict containing keys 'data', 'layout'.",  # noqa: E501
                "Those keys have the following types:",
                "  - data (list of dicts; optional): data is a collection of traces",  # noqa: E501
                "  - layout (dict; optional): layout describes the rest of the figure"  # noqa: E501

            ])],

            ['optionalObjectWithShapeAndNestedDescription', '\n'.join([

                "dict containing keys 'color', 'fontSize', 'figure'.",
                "Those keys have the following types:",
                "  - color (string; optional)",
                "  - fontSize (number; optional)",
                "  - figure (optional): Figure is a plotly graph object. figure has the following type: dict containing keys 'data', 'layout'.",  # noqa: E501
                "Those keys have the following types:",
                "  - data (list of dicts; optional): data is a collection of traces",  # noqa: E501
                "  - layout (dict; optional): layout describes the rest of the figure"  # noqa: E501

            ])],

            ['optionalAny', 'boolean | number | string | dict | list'],

            ['customProp', ''],

            ['customArrayProp', 'list'],

            ['data-*', 'string'],

            ['aria-*', 'string'],

            ['in', 'string'],

            ['id', 'string']
        ])