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

def test_get_ray_wheels_url(remove_buildkite_env):
    url = get_ray_wheels_url(
        repo_url="https://github.com/ray-project/ray.git",
        branch="master",
        commit="1234",
        ray_version="3.0.0.dev0",
    )
    assert (
        url == "https://s3-us-west-2.amazonaws.com/ray-wheels/master/1234/"
        "ray-3.0.0.dev0-cp37-cp37m-manylinux2014_x86_64.whl"
    )