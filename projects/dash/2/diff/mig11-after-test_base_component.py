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


class TestComponent:
    def test_to_plotly_json_with_nested_children_with_mixed_strings_and_without_lists(self):  # noqa: E501
        c = nested_tree()[0]
        Component._namespace
        Component._type

        expected = {
            'type': 'TestComponent',
            'namespace': 'test_namespace',
            'props': {
                'children': [
                    {
                        'type': 'TestComponent',
                        'namespace': 'test_namespace',
                        'props': {
                            'id': '0.0'
                        }
                    },
                    {
                        'type': 'TestComponent',
                        'namespace': 'test_namespace',
                        'props': {
                            'children': {
                                'type': 'TestComponent',
                                'namespace': 'test_namespace',
                                'props': {
                                    'children': {
                                        'type': 'TestComponent',
                                        'namespace': 'test_namespace',
                                        'props': {
                                            'children': [
                                                10,
                                                None,
                                                'wrap string',
                                                {
                                                    'type': 'TestComponent',
                                                    'namespace': 'test_namespace',  # noqa: E501
                                                    'props': {
                                                        'children': 'string',
                                                        'id': '0.1.x.x.0'
                                                    }
                                                },
                                                'another string',
                                                4.51
                                            ],
                                            'id': '0.1.x.x'
                                        }
                                    },
                                    'id': '0.1.x'
                                }
                            },
                            'id': '0.1'
                        }
                    }
                ],
                'id': '0'
            }
        }
        res = json.loads(json.dumps(
            c.to_plotly_json(),
            cls=plotly.utils.PlotlyJSONEncoder
        ))
        assert res == expected