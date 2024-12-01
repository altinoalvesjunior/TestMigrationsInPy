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
            
def test_dash_env_vars(empty_environ):
    assert {None} == {
        val for _, val in DASH_ENV_VARS.items()
    }, "initial var values are None without extra OS environ setting"