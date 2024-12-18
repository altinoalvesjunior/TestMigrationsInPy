import json
import os
import shutil
import unittest
from dash.development.component_loader import load_components, generate_classes
from dash.development.base_component import (
    Component
)
from dash.development._py_components_generation import generate_class

METADATA_PATH = 'metadata.json'

METADATA_STRING = '''{
    "MyComponent.react.js": {
        "props": {
            "foo": {
                "type": {
                    "name": "number"
                },
                "required": false,
                "description": "Description of prop foo.",
                "defaultValue": {
                    "value": "42",
                    "computed": false
                }
            },
            "children": {
                "type": {
                    "name": "object"
                },
                "description": "Children",
                "required": false
            },
            "data-*": {
                "type": {
                    "name": "string"
                },
                "description": "Wildcard data",
                "required": false
            },
            "aria-*": {
                "type": {
                    "name": "string"
                },
                "description": "Wildcard aria",
                "required": false
            },
            "bar": {
                "type": {
                    "name": "custom"
                },
                "required": false,
                "description": "Description of prop bar.",
                "defaultValue": {
                    "value": "21",
                    "computed": false
                }
            },
            "baz": {
                "type": {
                    "name": "union",
                    "value": [
                        {
                            "name": "number"
                        },
                        {
                            "name": "string"
                        }
                    ]
                },
                "required": false,
                "description": ""
            }
        },
        "description": "General component description.",
        "methods": []
    },
    "A.react.js": {
        "description": "",
        "methods": [],
        "props": {
            "href": {
                "type": {
                    "name": "string"
                },
                "required": false,
                "description": "The URL of a linked resource."
            },
            "children": {
                "type": {
                    "name": "object"
                },
                "description": "Children",
                "required": false
            }
        }
    }
}'''
METADATA = json\
    .JSONDecoder(object_pairs_hook=collections.OrderedDict)\
    .decode(METADATA_STRING)

class TestGenerateClasses(unittest.TestCase):
    def test_loadcomponents(self):
            MyComponent_runtime = generate_class(
                'MyComponent',
                METADATA['MyComponent.react.js']['props'],
                METADATA['MyComponent.react.js']['description'],
                'default_namespace'
            )

            A_runtime = generate_class(
                'A',
                METADATA['A.react.js']['props'],
                METADATA['A.react.js']['description'],
                'default_namespace'
            )

            generate_classes('default_namespace', METADATA_PATH)
            from default_namespace.MyComponent import MyComponent \
                as MyComponent_buildtime
            from default_namespace.A import A as A_buildtime

            MyComponentKwargs = {
                'foo': 'Hello World',
                'bar': 'Lah Lah',
                'baz': 'Lemons',
                'data-foo': 'Blah',
                'aria-bar': 'Seven',
                'children': 'Child'
            }
            AKwargs = {
                'children': 'Child',
                'href': 'Hello World'
            }

            self.assertTrue(
                isinstance(
                    MyComponent_buildtime(**MyComponentKwargs),
                    Component
                )
            )

            self.assertEqual(
                repr(MyComponent_buildtime(**MyComponentKwargs)),
                repr(MyComponent_runtime(**MyComponentKwargs)),
            )

            self.assertEqual(
                repr(A_runtime(**AKwargs)),
                repr(A_buildtime(**AKwargs))
            )