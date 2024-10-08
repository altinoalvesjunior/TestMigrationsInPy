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

@patch("ray_release.wheels.get_ray_version", lambda *a, **kw: "3.0.0.dev0")
def test_find_ray_wheels_branch(remove_buildkite_env):
    repo = DEFAULT_REPO
    branch = "master"
    commit = "1234" * 10
    version = "3.0.0.dev0"
    search_str = "master"
    _test_find_ray_wheels_checkout(repo, branch, commit, version, search_str)