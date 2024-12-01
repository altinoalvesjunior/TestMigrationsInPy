import os
import pytest
from flask import Flask
from dash import Dash, exceptions as _exc

from dash._configs import (
    pathname_configs,
    DASH_ENV_VARS,
    get_combined_config,
    load_dash_env_vars,
)
from dash._utils import get_asset_path


@pytest.fixture
def empty_environ():
    for k in DASH_ENV_VARS.keys():
        if k in os.environ:
            os.environ.pop(k)

def test_load_dash_env_vars_refects_to_os_environ(empty_environ):
    for var in DASH_ENV_VARS.keys():
        os.environ[var] = "true"
        vars = load_dash_env_vars()
        assert vars[var] == "true"
        os.environ[var] = "false"
        vars = load_dash_env_vars()
        assert vars[var] == "false"