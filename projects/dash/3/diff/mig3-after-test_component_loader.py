import json
import os
import shutil
import pytest
from dash.development._py_components_generation import generate_class
from dash.development.base_component import (
    Component
)
from dash.development.component_loader import load_components, generate_classes

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
    
class TestGenerateClasses:

    @pytest.fixture(autouse=True)
    def setup_function(self):
        with open(METADATA_PATH, 'w') as f:
            f.write(METADATA_STRING)
        os.makedirs('default_namespace')

        init_file_path = 'default_namespace/__init__.py'
        with open(init_file_path, 'a'):
            os.utime(init_file_path, None)
        yield
        os.remove(METADATA_PATH)
        shutil.rmtree('default_namespace')