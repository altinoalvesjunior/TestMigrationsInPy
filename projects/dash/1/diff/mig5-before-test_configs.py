import os
import unittest
import pytest
from flask import Flask

# noinspection PyProtectedMember

from dash._configs import (
    pathname_configs, DASH_ENV_VARS, get_combined_config, load_dash_env_vars)
from dash import Dash, exceptions as _exc
from dash._utils import get_asset_path


class TestConfigs(unittest.TestCase):

    def setUp(self):
        for k in DASH_ENV_VARS.keys():
            if k in os.environ:
                os.environ.pop(k)
    
    def test_pathname_prefix_environ_routes(self):
        os.environ['DASH_ROUTES_PATHNAME_PREFIX'] = '/routes/'
        _, routes, _ = pathname_configs()
        self.assertEqual('/routes/', routes)