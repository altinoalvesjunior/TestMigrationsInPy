import os
import sys
import time
import pytest
from unittest.mock import patch

@patch("ray_release.wheels.get_ray_version", lambda *a, **kw: "3.0.0.dev0")
def test_find_ray_wheels_buildkite(remove_buildkite_env):
    repo = DEFAULT_REPO
    branch = "master"
    commit = "1234" * 10
    version = "3.0.0.dev0"

    os.environ["BUILDKITE_COMMIT"] = commit

    url = find_ray_wheels_url()

    assert url == get_ray_wheels_url(repo, branch, commit, version)
    branch = "branched"
    os.environ["BUILDKITE_BRANCH"] = branch
    url = find_ray_wheels_url()
    assert url == get_ray_wheels_url(repo, branch, commit, version)