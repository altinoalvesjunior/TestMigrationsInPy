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

class TestFlowMetaDataConversions:
    @pytest.fixture(autouse=True)
    def setup_function(self):
        path = os.path.join(_dir, 'flow_metadata_test.json')
        with open(path) as data_file:
            json_string = data_file.read()
            data = json\
                .JSONDecoder(object_pairs_hook=OrderedDict)\
                .decode(json_string)
            self.data = data

        self.expected_arg_strings = OrderedDict([
            ['children', 'a list of or a singular dash component, string or number'],  # noqa: E501

            ['requiredString', 'string'],

            ['optionalString', 'string'],

            ['optionalBoolean', 'boolean'],

            ['optionalFunc', ''],

            ['optionalNode', 'a list of or a singular dash component, string or number'],  # noqa: E501

            ['optionalArray', 'list'],

            ['requiredUnion', 'string | number'],

            ['optionalSignature(shape)', '\n'.join([

                "dict containing keys 'checked', 'children', 'customData', 'disabled', 'label', 'primaryText', 'secondaryText', 'style', 'value'.",  # noqa: E501
                "Those keys have the following types:",
                "- checked (boolean; optional)",
                "- children (a list of or a singular dash component, string or number; optional)",  # noqa: E501
                "- customData (bool | number | str | dict | list; required): A test description",  # noqa: E501
                "- disabled (boolean; optional)",
                "- label (string; optional)",
                "- primaryText (string; required): Another test description",
                "- secondaryText (string; optional)",
                "- style (dict; optional)",
                "- value (bool | number | str | dict | list; required)"

            ])],

            ['requiredNested', '\n'.join([

                "dict containing keys 'customData', 'value'.",
                "Those keys have the following types:",
                "- customData (required): . customData has the following type: dict containing keys 'checked', 'children', 'customData', 'disabled', 'label', 'primaryText', 'secondaryText', 'style', 'value'.",  # noqa: E501
                "  Those keys have the following types:",
                "  - checked (boolean; optional)",
                "  - children (a list of or a singular dash component, string or number; optional)",  # noqa: E501
                "  - customData (bool | number | str | dict | list; required)",
                "  - disabled (boolean; optional)",
                "  - label (string; optional)",
                "  - primaryText (string; required)",
                "  - secondaryText (string; optional)",
                "  - style (dict; optional)",
                "  - value (bool | number | str | dict | list; required)",
                "- value (bool | number | str | dict | list; required)",

            ])],
        ])