import os
import sys
import time
import pytest
from unittest.mock import patch

from freezegun import freeze_time

from ray_release.config import Test
from ray_release.template import load_test_cluster_env
from ray_release.exception import RayWheelsNotFoundError, RayWheelsTimeoutError
from ray_release.util import url_exists
from ray_release.wheels import (
    get_ray_version,
    DEFAULT_REPO,
    get_ray_wheels_url,
    find_ray_wheels_url,
    find_and_wait_for_ray_wheels_url,
    is_wheels_url_matching_ray_verison,
    get_wheels_filename,
    maybe_rewrite_wheels_url,
)

def test_wheels_sanity_string(remove_buildkite_env):
    this_env = {"env": None}

    def override_env(path, env):
        this_env["env"] = env

    with patch(
        "ray_release.template.load_and_render_yaml_template", override_env
    ), patch("ray_release.template.get_test_environment", lambda: {}):
        load_test_cluster_env(
            Test(cluster=dict(cluster_env="invalid")),
            ray_wheels_url="https://no-commit-url",
        )
        assert "No commit sanity check" in this_env["env"]["RAY_WHEELS_SANITY_CHECK"]
        sha = "abcdef1234abcdef1234abcdef1234abcdef1234"
        load_test_cluster_env(
            Test(cluster=dict(cluster_env="invalid")),
            ray_wheels_url=f"https://some/{sha}/binary.whl",
        )
        assert sha in this_env["env"]["RAY_WHEELS_SANITY_CHECK"]