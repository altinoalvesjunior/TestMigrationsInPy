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


class TestLoadComponents(unittest.TestCase):
    def setUp(self):
        with open(METADATA_PATH, 'w') as f:
            f.write(METADATA_STRING)
    def tearDown(self):
        os.remove(METADATA_PATH)