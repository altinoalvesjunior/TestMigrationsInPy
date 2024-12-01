import os
import unittest
import pytest
from flask import Flask

from dash._configs import (
    pathname_configs, DASH_ENV_VARS, get_combined_config, load_dash_env_vars)
from dash import Dash, exceptions as _exc
from dash._utils import get_asset_path


class TestConfigs(unittest.TestCase):

    def setUp(self):
        for k in DASH_ENV_VARS.keys():
            if k in os.environ:
                os.environ.pop(k)
    
    def test_get_combined_config_props_check(self):
        val1 = get_combined_config('props_check', None, default=False)
        self.assertEqual(
            val1, False,
            "should return the default value if None is provided for init and environment")
        os.environ['DASH_PROPS_CHECK'] = 'true'
        val2 = get_combined_config('props_check', None, default=False)
        self.assertEqual(val2, True, "should return the set environment value as True")
        val3 = get_combined_config('props_check', False, default=True)
        self.assertEqual(val3, False, "init value overrides the environment value")