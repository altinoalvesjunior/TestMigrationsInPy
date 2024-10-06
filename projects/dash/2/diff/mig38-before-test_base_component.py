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


def nested_tree():
    """This tree has a few unique properties:
    - children is mixed strings and components (as in c2)
    - children is just components (as in c)
    - children is just strings (as in c1)
    - children is just a single component (as in c3, c4)
    - children contains numbers (as in c2)
    - children contains "None" items (as in c2)
    """
    c1 = Component(
        id='0.1.x.x.0',
        children='string'
    )
    c2 = Component(
        id='0.1.x.x',
        children=[10, None, 'wrap string', c1, 'another string', 4.51]
    )
    c3 = Component(
        id='0.1.x',
        # children is just a component
        children=c2
    )
    c4 = Component(
        id='0.1',
        children=c3
    )
    c5 = Component(id='0.0')
    c = Component(id='0', children=[c5, c4])
    return c, c1, c2, c3, c4, c5


class TestMetaDataConversions(unittest.TestCase):
    def setUp(self):
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
                "  - data (list of dicts; optional): data is a collection of traces",
                "  - layout (dict; optional): layout describes the rest of the figure"  # noqa: E501

            ])],

            ['optionalObjectWithShapeAndNestedDescription', '\n'.join([

                "dict containing keys 'color', 'fontSize', 'figure'.",
                "Those keys have the following types:",
                "  - color (string; optional)",
                "  - fontSize (number; optional)",
                "  - figure (optional): Figure is a plotly graph object. figure has the following type: dict containing keys 'data', 'layout'.",  # noqa: E501
                "Those keys have the following types:",
                "  - data (list of dicts; optional): data is a collection of traces",
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
        
        def test_docgen_to_python_args(self):
            props = self.data['props']

            for prop_name, prop in list(props.items()):
                self.assertEqual(
                    js_to_py_type(prop['type']),
                    self.expected_arg_strings[prop_name]
                )