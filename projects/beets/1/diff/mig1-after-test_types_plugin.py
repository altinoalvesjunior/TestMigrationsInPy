import time
from datetime import datetime

import pytest
from confuse import ConfigValueError

from beets.test.helper import PluginTestCase


class TypesPluginTest(PluginTestCase):
    plugin = "types"

def test_unknown_type_error(self):
        self.config["types"] = {"flex": "unkown type"}
        with pytest.raises(ConfigValueError):
            self.run_command("ls")