import os
import sys
import time
import pytest
from unittest.mock import patch

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
