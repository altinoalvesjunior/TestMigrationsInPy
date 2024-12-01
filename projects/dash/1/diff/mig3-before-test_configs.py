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
    
    def test_invalid_pathname_prefix(self):
        with self.assertRaises(_exc.InvalidConfig) as context:
            _, _, _ = pathname_configs('/my-path', '/another-path')
            self.assertTrue('url_base_pathname' in str(context.exception))
        with self.assertRaises(_exc.InvalidConfig) as context:
            _, _, _ = pathname_configs(
                url_base_pathname='/invalid',
                routes_pathname_prefix='/invalid')
            self.assertTrue(str(context.exception).split('.')[0]
                            .endswith('`routes_pathname_prefix`'))
        with self.assertRaises(_exc.InvalidConfig) as context:
            _, _, _ = pathname_configs(
                url_base_pathname='/my-path',
                requests_pathname_prefix='/another-path')
            self.assertTrue(str(context.exception).split('.')[0]
                            .endswith('`requests_pathname_prefix`'))
        with self.assertRaises(_exc.InvalidConfig) as context:
            _, _, _ = pathname_configs('my-path')
            self.assertTrue('start with `/`' in str(context.exception))
        with self.assertRaises(_exc.InvalidConfig) as context:
            _, _, _ = pathname_configs('/my-path')
            self.assertTrue('end with `/`' in str(context.exception))