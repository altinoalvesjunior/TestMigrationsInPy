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

def test_invalid_pathname_prefix(empty_environ):
    with pytest.raises(_exc.InvalidConfig, match="url_base_pathname"):
        _, _, _ = pathname_configs("/my-path", "/another-path")

    with pytest.raises(_exc.InvalidConfig) as excinfo:
        _, _, _ = pathname_configs(
            url_base_pathname="/invalid", routes_pathname_prefix="/invalid"
        )
    assert str(excinfo.value).split(".")[0].endswith("`routes_pathname_prefix`")

    with pytest.raises(_exc.InvalidConfig) as excinfo:
        _, _, _ = pathname_configs(
            url_base_pathname="/my-path", requests_pathname_prefix="/another-path"
        )
    assert str(excinfo.value).split(".")[0].endswith("`requests_pathname_prefix`")
    with pytest.raises(_exc.InvalidConfig, match="start with `/`"):
        _, _, _ = pathname_configs("my-path")
    with pytest.raises(_exc.InvalidConfig, match="end with `/`"):
        _, _, _ = pathname_configs("/my-path")