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

def test_matching_ray_wheels_url():
    assert not is_wheels_url_matching_ray_verison(
        f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 8))}", (3, 7)
    )

    assert not is_wheels_url_matching_ray_verison(
        f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}", (3, 8)
    )

    assert is_wheels_url_matching_ray_verison(
        f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}", (3, 7)
    )


@patch("ray_release.wheels.resolve_url", lambda url: url)
def test_rewrite_wheels_url(remove_buildkite_env):
    # Do not rewrite if versions match
    assert (
        maybe_rewrite_wheels_url(
            f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}",
            (3, 7),
        )
        == f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}"
    )
    # Do not rewrite if version can't be parsed
    assert (
        maybe_rewrite_wheels_url("http://some/location/unknown.whl", (3, 7))
        == "http://some/location/unknown.whl"
    )
    # Rewrite when version can be parsed
    assert (
        maybe_rewrite_wheels_url(
            f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 8))}",
            (3, 7),
        )
        == f"http://some/location/{get_wheels_filename('3.0.0dev0', (3, 7))}"
    )