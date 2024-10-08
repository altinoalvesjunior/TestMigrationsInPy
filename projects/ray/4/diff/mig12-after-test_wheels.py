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

def _test_find_ray_wheels_checkout(
    repo: str, branch: str, commit: str, version: str, search_str: str
):
    with patch(
        "ray_release.wheels.get_latest_commits", lambda *a, **kw: [commit]
    ), patch("ray_release.wheels.url_exists", lambda *a, **kw: False), pytest.raises(
        RayWheelsNotFoundError
    ):
        # Fails because URL does not exist
        find_ray_wheels_url(search_str)

    with patch(
        "ray_release.wheels.get_latest_commits", lambda *a, **kw: [commit]
    ), patch("ray_release.wheels.url_exists", lambda *a, **kw: True):
        # Succeeds
        url = find_ray_wheels_url(search_str)

        assert url == get_ray_wheels_url(repo, branch, commit, version)
