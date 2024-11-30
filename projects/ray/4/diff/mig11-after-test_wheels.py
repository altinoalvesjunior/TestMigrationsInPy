import os
import sys
import time
import pytest
from unittest.mock import patch

@patch("time.sleep", lambda *a, **kw: None)
@patch("ray_release.wheels.get_ray_version", lambda *a, **kw: "3.0.0.dev0")
def test_find_and_wait_wheels(remove_buildkite_env):
    repo = DEFAULT_REPO
    branch = "master"
    commit = "1234" * 10
    version = "3.0.0.dev0"
    class TrueAfter:
        def __init__(self, after: float):
            self.available_at = time.monotonic() + after
        def __call__(self, *args, **kwargs):
            if time.monotonic() > self.available_at:
                return True
            return False
    with freeze_time(auto_tick_seconds=10):
        with patch("ray_release.wheels.url_exists", TrueAfter(400)):
            with pytest.raises(RayWheelsTimeoutError):
                find_and_wait_for_ray_wheels_url(commit, timeout=300.0)

    with freeze_time(auto_tick_seconds=10):
        with patch("ray_release.wheels.url_exists", TrueAfter(200)):
            url = find_and_wait_for_ray_wheels_url(commit, timeout=300.0)

        assert url == get_ray_wheels_url(repo, branch, commit, version)