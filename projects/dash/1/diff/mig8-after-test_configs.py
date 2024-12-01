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

def test_get_combined_config_props_check(empty_environ):
    val1 = get_combined_config("props_check", None, default=False)
    assert (
        not val1
    ), "should return the default value if None is provided for init and environment"
    os.environ["DASH_PROPS_CHECK"] = "true"
    val2 = get_combined_config("props_check", None, default=False)
    assert val2, "should return the set environment value as True"
    val3 = get_combined_config("props_check", False, default=True)
    assert not val3, "init value overrides the environment value"